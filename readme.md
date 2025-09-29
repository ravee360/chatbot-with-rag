# RAG_Project

A modular Retrieval-Augmented Generation (RAG) application with document management, chat history, and LangChain-powered LLM integration. This project provides a robust backend and Streamlit-based frontend for uploading documents, querying them with LLMs, and managing chat and document metadata.

---
# [Live Demo on Streamlit 🚀](https://raviloveschatbot232326.streamlit.app/)

---
## Features

- **Document Upload & Management:**  
  Upload PDF, DOCX, and HTML files. Metadata is stored in SQLite for easy retrieval and management.

- **RAG Chatbot:**  
  Ask questions about your uploaded documents. The system retrieves relevant context and generates answers using a Large Language Model (LLM) via LangChain.

- **Chat History:**  
  All user queries and LLM responses are logged and can be retrieved per session.

- **Vector Store Integration:**  
  Documents are indexed into a vector store (ChromaDB by default) for efficient retrieval.

- **Modular Codebase:**  
  Clean separation of database utilities, vector store logic, and LangChain pipeline for easy extension and maintenance.

- **Streamlit Frontend:**  
  User-friendly web interface for document upload, chat, and document management.

- **FastAPI Backend (Optional):**  
  RESTful API endpoints for document upload, querying, and management, suitable for integration with other services or custom frontends.

---

## Folder Structure

```
RAG_Project/
│
├── app.py                   # Streamlit frontend
├── main.py                  # FastAPI backend (optional)
├── db_utils.py              # Database utilities for main app
├── db_utils_tele_bot.py     # Database utilities for Telegram bot
├── chroma_utils.py          # Vector store utilities
├── langchain_utils.py       # LangChain RAG pipeline
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (local use)
├── .streamlit/
│   └── secrets.toml         # Streamlit secrets (for deployment)
├── uploaded_docs/           # Uploaded document storage
└── README.md                # Project documentation
```

---

## Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_Project.git
cd RAG_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

- For local development, create a `.env` file with your API keys and settings.
- For Streamlit Cloud, add secrets in the `.streamlit/secrets.toml` file or via the web UI.

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

- The app will be available at [http://localhost:8501](http://localhost:8501).

### 5. (Optional) Run the FastAPI Backend

```bash
uvicorn main:app --reload
```

- The API will be available at [http://localhost:8000](http://localhost:8000).

---

## Configuration

- **API Keys:**  
  Store your OpenAI or other LLM provider keys in `.env` or Streamlit secrets.
- **Vector Store:**  
  By default, uses ChromaDB. You can configure or swap out for other vector stores in `chroma_utils.py`.
- **Database:**  
  Uses SQLite for metadata and chat logs. For production, consider a managed database.

---

## Customization

- **Add new document types:**  
  Extend `chroma_utils.py` and `app.py` to support more file formats.
- **Change LLM or RAG pipeline:**  
  Modify `langchain_utils.py` to use different models or retrieval strategies.
- **Integrate with other frontends:**  
  The backend logic is modular and can be reused in other interfaces.

---

## Example Usage

1. **Upload a Document:**  
   Use the Streamlit interface to upload a PDF, DOCX, or HTML file.

2. **Ask a Question:**  
   Enter a question in the chat interface. The system will retrieve relevant context from your uploaded documents and generate an answer using the configured LLM.

3. **View Chat History:**  
   All interactions are logged and can be reviewed per session.

4. **Manage Documents:**  
   List, delete, or upload new documents as needed.

---

## Troubleshooting

- **Secrets Not Found:**  
  Ensure your `.env` or `.streamlit/secrets.toml` is correctly configured with all required API keys.
- **File Persistence on Streamlit Cloud:**  
  Uploaded files and local SQLite databases are not persistent on Streamlit Community Cloud. Use external storage for production.
- **Vector Store Issues:**  
  If using ChromaDB in persistent mode, ensure you have the correct permissions and storage paths.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Streamlit](https://github.com/streamlit/streamlit)
```# RAG_Project

A modular Retrieval-Augmented Generation (RAG) application with document management, chat history, and LangChain-powered LLM integration. This project provides a robust backend and Streamlit-based frontend for uploading documents, querying them with LLMs, and managing chat and document metadata.

---

## Features

- **Document Upload & Management:**  
  Upload PDF, DOCX, and HTML files. Metadata is stored in SQLite for easy retrieval and management.

- **RAG Chatbot:**  
  Ask questions about your uploaded documents. The system retrieves relevant context and generates answers using a Large Language Model (LLM) via LangChain.

- **Chat History:**  
  All user queries and LLM responses are logged and can be retrieved per session.

- **Vector Store Integration:**  
  Documents are indexed into a vector store (ChromaDB by default) for efficient retrieval.

- **Modular Codebase:**  
  Clean separation of database utilities, vector store logic, and LangChain pipeline for easy extension and maintenance.

- **Streamlit Frontend:**  
  User-friendly web interface for document upload, chat, and document management.

- **FastAPI Backend (Optional):**  
  RESTful API endpoints for document upload, querying, and management, suitable for integration with other services or custom frontends.

---

## Folder Structure

```
RAG_Project/
│
├── app.py                   # Streamlit frontend
├── main.py                  # FastAPI backend (optional)
├── db_utils.py              # Database utilities for main app
├── db_utils_tele_bot.py     # Database utilities for Telegram bot
├── chroma_utils.py          # Vector store utilities
├── langchain_utils.py       # LangChain RAG pipeline
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (local use)
├── .streamlit/
│   └── secrets.toml         # Streamlit secrets (for deployment)
├── uploaded_docs/           # Uploaded document storage
└── README.md                # Project documentation
```

---

## Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_Project.git
cd RAG_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

- For local development, create a `.env` file with your API keys and settings.
- For Streamlit Cloud, add secrets in the `.streamlit/secrets.toml` file or via the web UI.

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

- The app will be available at [http://localhost:8501](http://localhost:8501).

### 5. (Optional) Run the FastAPI Backend

```bash
uvicorn main:app --reload
```

- The API will be available at [http://localhost:8000](http://localhost:8000).

---

## Configuration

- **API Keys:**  
  Store your OpenAI or other LLM provider keys in `.env` or Streamlit secrets.
- **Vector Store:**  
  By default, uses ChromaDB. You can configure or swap out for other vector stores in `chroma_utils.py`.
- **Database:**  
  Uses SQLite for metadata and chat logs. For production, consider a managed database.

---

## Customization

- **Add new document types:**  
  Extend `chroma_utils.py` and `app.py` to support more file formats.
- **Change LLM or RAG pipeline:**  
  Modify `langchain_utils.py` to use different models or retrieval strategies.
- **Integrate with other frontends:**  
  The backend logic is modular and can be reused in other interfaces.

---

## Example Usage

1. **Upload a Document:**  
   Use the Streamlit interface to upload a PDF, DOCX, or HTML file.

2. **Ask a Question:**  
   Enter a question in the chat interface. The system will retrieve relevant context from your uploaded documents and generate an answer using the configured LLM.

3. **View Chat History:**  
   All interactions are logged and can be reviewed per session.

4. **Manage Documents:**  
   List, delete, or upload new documents as needed.

---

## Troubleshooting

- **Secrets Not Found:**  
  Ensure your `.env` or `.streamlit/secrets.toml` is correctly configured with all required API keys.
- **File Persistence on Streamlit Cloud:**  
  Uploaded files and local SQLite databases are not persistent on Streamlit Community Cloud. Use external storage for production.
- **Vector Store Issues:**  
  If using ChromaDB in persistent mode, ensure you have the correct permissions and storage paths.

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Streamlit](https://github.com/streamlit/streamlit)
