import os
import uuid
import requests
import streamlit as st

# --- Config ---
DEFAULT_API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

# --- Helpers ---
def api_base():
    return st.session_state.get("api_base", DEFAULT_API_BASE)

def post_json(endpoint, payload, timeout=60):
    resp = requests.post(f"{api_base()}{endpoint}", json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def get_json(endpoint, timeout=60):
    resp = requests.get(f"{api_base()}{endpoint}", timeout=timeout)
    resp.raise_for_status()
    return resp.json()

# --- API Calls ---
def chat_api(question):
    return post_json("/chat", {
        "question": question,
        "session_id": st.session_state.session_id,
        "model": st.session_state.model
    }, timeout=120)["answer"]

def upload_doc(file):
    file_bytes = file.getvalue()
    content_type = getattr(file, "type", None) or "application/octet-stream"
    files = {"file": (file.name, file_bytes, content_type)}
    resp = requests.post(f"{api_base()}/upload-doc", files=files, timeout=300)
    resp.raise_for_status()
    return resp.json().get("message", "Uploaded")

def list_docs():
    return get_json("/list-docs")

def delete_doc(file_id):
    return post_json("/delete-doc", {"file_id": file_id}).get("message", "Deleted")

# --- Init State ---
def init_state():
    st.session_state.setdefault("session_id", str(uuid.uuid4()))
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("model", "gpt-4o-mini")
    st.session_state.setdefault("api_base", DEFAULT_API_BASE)
    st.session_state.setdefault("docs", [])
    st.session_state.setdefault("uploading", False)
    st.session_state.setdefault("api_ok", None)

# --- Sidebar ---
def sidebar():
    st.sidebar.header("⚙️ Settings")
    st.sidebar.text_input("API Base", key="api_base")
    st.sidebar.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], key="model")

    col_h1, col_h2 = st.sidebar.columns(2)
    if col_h1.button("Health"):
        try:
            _ = list_docs()
            st.session_state.api_ok = True
            col_h1.success("OK")
        except Exception as e:
            st.session_state.api_ok = False
            col_h1.error("Fail")

    st.sidebar.header("📄 Documents")
    with st.sidebar.form(key="upload_form", clear_on_submit=True):
        file = st.file_uploader("Upload", type=["pdf", "docx", "html"])
        submitted = st.form_submit_button("Upload")
        if submitted and file is not None:
            st.session_state.uploading = True
            try:
                st.success(upload_doc(file))
                st.session_state.docs = list_docs()
                st.session_state.uploading = False
                st.rerun()
            except Exception as e:
                st.session_state.uploading = False
                st.error(f"Upload failed: {e}")

    if st.sidebar.button("Refresh list"):
        try:
            st.session_state.docs = list_docs()
        except Exception as e:
            st.sidebar.error(f"List failed: {e}")

    if not st.session_state.docs:
        try:
            st.session_state.docs = list_docs()
        except Exception:
            pass

    if st.session_state.docs:
        st.sidebar.markdown("Uploaded:")
        for d in st.session_state.docs:
            st.sidebar.write(f"- {d['filename']}")

        doc_map = {d["filename"]: d["id"] for d in st.session_state.docs}
        to_delete = st.sidebar.selectbox("Delete document", list(doc_map.keys()))
        if st.sidebar.button("Delete"):
            try:
                st.sidebar.success(delete_doc(doc_map[to_delete]))
                st.session_state.docs = list_docs()
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Delete failed: {e}")
    else:
        st.sidebar.info("No documents uploaded yet.")

# --- Chat UI ---
def chat_ui():
    st.title("💬 LangChain RAG Chatbot")
    if st.session_state.uploading:
        st.info("Uploading…")

    if not st.session_state.docs:
        st.warning("Upload a document first to enable retrieval.")

    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)

    prompt = st.chat_input("Ask about your documents...")
    if prompt:
        st.session_state.messages.append(("user", prompt))
        try:
            answer = chat_api(prompt)
            st.session_state.messages.append(("assistant", answer))
        except Exception as e:
            st.session_state.messages.append(("assistant", f"Error: {e}"))
        st.rerun()

# --- Main ---
def main():
    st.set_page_config(page_title="RAG App", page_icon="📚", layout="wide")
    init_state()
    sidebar()
    chat_ui()

if __name__ == "__main__":
    main()
