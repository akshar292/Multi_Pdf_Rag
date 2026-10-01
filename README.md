# 📚 Multi-PDF RAG System

A **Multi-PDF Retrieval-Augmented Generation (RAG)** application that allows users to upload multiple PDF documents and ask questions about their content using **semantic search, ChromaDB, LangGraph, and Groq AI**.

The system retrieves relevant information from uploaded PDFs and uses a Groq-powered LLM to generate answers based only on the retrieved document content.

---

## 🚀 Features

- 📄 Upload multiple PDF documents
- 🔍 Semantic search across uploaded PDFs
- 🧠 Retrieval-Augmented Generation (RAG)
- 🗂️ ChromaDB vector database
- 🔗 LangGraph workflow
- ⚡ Groq AI for fast LLM responses
- 🤖 `openai/gpt-oss-120b` model through Groq
- 📑 Display document sources and page numbers
- 🌐 React + Vite frontend
- 🐍 FastAPI backend
- 🔐 Environment-variable based API keys
- 📱 Simple and responsive interface

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │      React UI       │
                    │   Vite Frontend     │
                    └──────────┬──────────┘
                               │
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │ PDF Processing│             │   LangGraph   │
        │    pypdf      │             │    Workflow   │
        └───────┬───────┘             └───────┬───────┘
                │                             │
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │ Text Chunking │             │   Retrieval   │
        │ LangChain     │             │   ChromaDB    │
        └───────┬───────┘             └───────┬───────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    ┌─────────────────────┐
                    │      Groq LLM       │
                    │ openai/gpt-oss-120b │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Final Answer    │
                    │   + PDF Sources     │
                    └─────────────────────┘
```

---

## 🔄 RAG Workflow

The application follows this workflow:

```text
Upload PDF
     ↓
Extract PDF Text
     ↓
Split Text into Chunks
     ↓
Generate Embeddings
     ↓
Store in ChromaDB
     ↓
User Asks Question
     ↓
Semantic Similarity Search
     ↓
Retrieve Relevant Chunks
     ↓
Build Context
     ↓
LangGraph
     ↓
Groq LLM
     ↓
Generate Answer
     ↓
Return Answer + Sources
```

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- ChromaDB
- pypdf
- Sentence Transformers
- Groq API

### Frontend

- React
- Vite
- Axios
- JavaScript

### AI / RAG

- Retrieval-Augmented Generation
- Embeddings
- Vector Search
- Semantic Search
- LangGraph
- Groq LLM

---

## 📁 Project Structure

```text
Multi_Pdf_Rag/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rag.py
│   │   └── graph.py
│   │
│   ├── uploads/
│   │
│  
