import os

from dotenv import load_dotenv

load_dotenv()


from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from .rag import (
    save_uploaded_file,
    process_pdf
)

from .graph import ask_question


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="Multi-PDF RAG System",
    description="Multi-PDF RAG using LangGraph, ChromaDB and Groq",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Multi-PDF RAG API is running",
        "status": "success"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# UPLOAD RESPONSE
# =========================================================

class UploadResponse(BaseModel):

    filename: str

    chunks: int

    message: str


# =========================================================
# UPLOAD PDF
# =========================================================

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_pdf(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # VALIDATE FILE
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        file_path = save_uploaded_file(
            file,
            file.filename
        )

        # -------------------------------------------------
        # PROCESS
        # -------------------------------------------------

        chunks = process_pdf(
            file_path,
            file.filename
        )

        if chunks == 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text from "
                    "the PDF."
                )
            )

        return {

            "filename": file.filename,

            "chunks": chunks,

            "message": (
                "PDF uploaded and indexed successfully."
            )
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Upload error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ASK REQUEST
# =========================================================

class AskRequest(BaseModel):

    question: str


# =========================================================
# ASK RESPONSE
# =========================================================

class AskResponse(BaseModel):

    answer: str

    sources: list


# =========================================================
# ASK
# =========================================================

@app.post(
    "/ask",
    response_model=AskResponse
)
async def ask(
    request: AskRequest
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = ask_question(
            question
        )

        return result

    except Exception as e:

        print(
            "Ask error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )