import os
import uuid
import shutil
import streamlit as st
from dotenv import load_dotenv

# Internal modules
from db_utils import (
    insert_application_logs,
    get_chat_history,
    get_all_documents,
    insert_document_record,
    delete_document_record,
)
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma
from langchain_utils import get_rag_chain


# --- Config ---
load_dotenv()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")


# --- Helpers ---
def ensure_state():
    st.session_state.setdefault("session_id", str(uuid.uuid4()))
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("model", DEFAULT_MODEL)
    st.session_state.setdefault("docs", [])
    st.session_state.setdefault("uploading", False)


def refresh_docs():
    try:
        st.session_state.docs = get_all_documents()
    except Exception as e:
        st.sidebar.error(f"List failed: {e}")


def handle_upload(file):
    temp_file_path = f"temp_{file.name}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.getvalue())

        # Metadata (size and type)
        try:
            size_bytes = len(file.getvalue())
        except Exception:
            size_bytes = None
        content_type = getattr(file, "type", None)

        file_id = insert_document_record(file.name, size_bytes, content_type)
        success = index_document_to_chroma(temp_file_path, file_id)

        if not success:
            delete_document_record(file_id)
            raise RuntimeError(f"Failed to index {file.name}")

        return f"File {file.name} has been successfully uploaded and indexed.", file_id
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def handle_delete(file_id: int):
    chroma_delete_success = delete_doc_from_chroma(file_id)
    if chroma_delete_success:
        db_delete_success = delete_document_record(file_id)
        if db_delete_success:
            return True, "Deleted"
        return False, "Deleted from Chroma but failed to delete from DB"
    return False, "Failed to delete from Chroma"


# --- Sidebar ---
def sidebar():
    st.sidebar.header("⚙️ Settings")
    st.sidebar.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], key="model")

    st.sidebar.header("📄 Documents")
    with st.sidebar.form(key="upload_form", clear_on_submit=True):
        file = st.file_uploader("Upload", type=["pdf", "docx", "html"])
        submitted = st.form_submit_button("Upload")
        if submitted and file is not None:
            st.session_state.uploading = True
            try:
                message, _ = handle_upload(file)
                st.success(message)
                refresh_docs()
                st.session_state.uploading = False
                st.rerun()
            except Exception as e:
                st.session_state.uploading = False
                st.error(f"Upload failed: {e}")

    if st.sidebar.button("Refresh list"):
        refresh_docs()

    if not st.session_state.docs:
        refresh_docs()

    if st.session_state.docs:
        st.sidebar.markdown("Uploaded:")
        for d in st.session_state.docs:
            st.sidebar.write(f"- {d['filename']}")

        doc_map = {d["filename"]: d["id"] for d in st.session_state.docs}
        to_delete = st.sidebar.selectbox("Delete document", list(doc_map.keys()))
        if st.sidebar.button("Delete"):
            try:
                ok, msg = handle_delete(doc_map[to_delete])
                if ok:
                    st.sidebar.success("Deleted")
                else:
                    st.sidebar.error(msg)
                refresh_docs()
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
            chat_history = get_chat_history(st.session_state.session_id)
            rag_chain = get_rag_chain(st.session_state.model)
            answer = rag_chain.invoke(
                {
                    "input": prompt,
                    "chat_history": chat_history
                },
                config={
                    "run_name": "RAG Chat",
                    "tags": ["streamlit", st.session_state.model]
                }
            )["answer"]

            st.session_state.messages.append(("assistant", answer))
            insert_application_logs(
                st.session_state.session_id,
                prompt,
                answer,
                st.session_state.model,
            )
        except Exception as e:
            st.session_state.messages.append(("assistant", f"Error: {e}"))
        st.rerun()


# --- Main ---
def main():
    st.set_page_config(page_title="RAG App", page_icon="📚", layout="wide")
    ensure_state()
    sidebar()
    chat_ui()


if __name__ == "__main__":
    main()


