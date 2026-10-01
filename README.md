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
│   ├── chroma_db/
│   │
│   ├── .env
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   │
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
│
└── README.md
```

---

# ⚙️ Backend Setup

## 1. Clone Repository

```bash
git clone https://github.com/akshar292/Multi_Pdf_Rag.git
```

Go inside the project:

```bash
cd Multi_Pdf_Rag
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If required, install the main packages manually:

```bash
pip install fastapi uvicorn
pip install langchain
pip install langgraph
pip install langchain-groq
pip install langchain-chroma
pip install langchain-huggingface
pip install sentence-transformers
pip install pypdf
pip install python-dotenv
pip install python-multipart
```

---

# 🔑 Environment Variables

Create a `.env` file inside the `backend` directory.

```env
GROQ_API_KEY=your_groq_api_key
```

Do **not** commit your API key to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
chroma_db/
uploads/
```

---

# 🤖 Groq Configuration

The project uses Groq through LangChain:

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

The LLM is responsible for generating the final answer from the retrieved PDF context.

---

# 🧠 Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This is a lightweight embedding model that generates **384-dimensional embeddings**.

Example:

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)
```

---

# 🗂️ ChromaDB

ChromaDB stores the document embeddings and metadata.

Each document chunk contains metadata such as:

```json
{
  "source": "example.pdf",
  "page": 1
}
```

This allows the application to return the PDF filename and page number along with the answer.

---

# 🔗 LangGraph

The RAG pipeline uses three main LangGraph nodes:

```text
START
  ↓
Retrieve
  ↓
Context
  ↓
Generate
  ↓
END
```

### Retrieve Node

Retrieves relevant PDF chunks from ChromaDB.

### Context Node

Combines retrieved chunks and prepares source information.

### Generate Node

Sends the retrieved context and user's question to the Groq LLM.

---

# 🌐 Running Backend

Go to the backend folder:

```powershell
cd backend
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Go to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

# 📄 Upload PDFs

The application supports uploading multiple PDF files.

Example:

```text
📄 nlp_fundamentals_rag_test.pdf
📄 python_fundamentals_rag_test.pdf
📄 machine_learning_rag_test.pdf
```

After clicking:

```text
Upload & Index PDFs
```

the backend:

1. Saves the PDF
2. Extracts text
3. Splits the text into chunks
4. Generates embeddings
5. Stores vectors in ChromaDB

---

# 💬 Ask Questions

After uploading PDFs, ask questions such as:

```text
What is TF-IDF?
```

```text
What is supervised learning?
```

```text
What is Python?
```

```text
Explain K-Means clustering.
```

The system retrieves relevant information and generates the answer using Groq.

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## Upload PDF

```http
POST /upload
```

Form-data:

```text
file: PDF file
```

Example response:

```json
{
  "filename": "machine_learning.pdf",
  "chunks": 12,
  "message": "PDF uploaded and indexed successfully."
}
```

---

## Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "What is TF-IDF?"
}
```

Example response:

```json
{
  "answer": "TF-IDF stands for Term Frequency-Inverse Document Frequency...",
  "sources": [
    {
      "file": "nlp_fundamentals_rag_test.pdf",
      "page": 1
    }
  ]
}
```

---

# 🔐 Security

Never upload API keys to GitHub.

Use:

```env
GROQ_API_KEY=your_api_key
```

and keep `.env` inside `.gitignore`.

If an API key is accidentally exposed, revoke it and generate a new one.

---

# ☁️ Deployment

The backend can be deployed as a FastAPI web service.

Example start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

For deployment platforms that provide a `$PORT` environment variable, use that variable instead of hardcoding `8000`.

---

# ⚠️ Deployment Notes

The application uses a local embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Therefore, the server needs enough RAM to load the embedding model.

The ChromaDB directory is also local:

```text
chroma_db/
```

On free hosting environments, local files may not be persistent between deployments/restarts. For a production application, persistent storage or an external vector database can be considered.

---

# 🧪 Testing

### Test Backend

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
GET /health
```

Then:

```text
POST /upload
```

Then:

```text
POST /ask
```

---

# 🐛 Common Issues

## 1. Chroma dimension mismatch

Example:

```text
Collection expecting embedding with dimension of 3072,
got 384
```

This means the existing ChromaDB was created using a different embedding model.

Delete the old database:

```powershell
Remove-Item -Recurse -Force .\chroma_db
```

Then restart the backend and upload the PDFs again.

---

## 2. Groq model not found

If you see:

```text
model_not_found
```

check the model configured in `graph.py` and use a currently available Groq model.

---

## 3. Missing Groq API Key

If you see:

```text
GROQ_API_KEY is not set
```

check your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Then restart the backend.

---

## 4. CORS Error

Make sure the frontend URL is included in the FastAPI CORS configuration.

For local development:

```text
http://localhost:5173
```

---

# 🎯 Project Goal

The goal of this project is to demonstrate how modern **RAG architecture** can be used to build a document-based AI assistant.

The project combines:

```text
Python
    +
FastAPI
    +
React
    +
LangChain
    +
LangGraph
    +
ChromaDB
    +
Embeddings
    +
Groq
    =
Multi-PDF AI Assistant
```

---

# 📌 Future Improvements

Possible future improvements include:

- 🔐 User authentication
- 💾 Persistent cloud vector database
- ☁️ Cloud file storage
- 📊 RAG evaluation
- 🔎 Improved retrieval using hybrid search
- 🧠 Reranking retrieved documents
- 💬 Chat history
- 📑 Better source citation
- 👥 Multiple users
- 📈 Usage analytics
- 🗃️ Document management
- 🌍 Production deployment

---

# 👨‍💻 Author

**Akshar Bhavsar**

Computer Engineering / AI & Data Science Project

GitHub:

```text
https://github.com/akshar292
```

---

## ⭐ If you find this project useful

Give the repository a ⭐ on GitHub.
