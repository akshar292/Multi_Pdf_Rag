import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# =========================================================
# ENV
# =========================================================

load_dotenv()


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# DOCUMENT STORAGE
# =========================================================

documents_store = []


# =========================================================
# TEXT SPLITTER
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# =========================================================
# PROCESS PDF
# =========================================================

def process_pdf(
    file_path: str,
    original_filename: str
):

    reader = PdfReader(file_path)

    documents = []

    # -----------------------------------------------------
    # READ PDF PAGES
    # -----------------------------------------------------

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        try:

            text = page.extract_text()

        except Exception as e:

            print(
                f"Error extracting page {page_number}: {e}"
            )

            continue

        if not text:
            continue

        text = text.strip()

        if not text:
            continue

        document = Document(
            page_content=text,
            metadata={
                "source": original_filename,
                "page": page_number
            }
        )

        documents.append(document)

    # -----------------------------------------------------
    # NO TEXT
    # -----------------------------------------------------

    if not documents:

        return 0

    # -----------------------------------------------------
    # CHUNKING
    # -----------------------------------------------------

    chunks = text_splitter.split_documents(
        documents
    )

    # -----------------------------------------------------
    # STORE DOCUMENTS
    # -----------------------------------------------------

    documents_store.extend(
        chunks
    )

    print(
        f"Indexed {len(chunks)} chunks from "
        f"{original_filename}"
    )

    return len(chunks)


# =========================================================
# SAVE UPLOADED FILE
# =========================================================

def save_uploaded_file(
    file,
    filename: str
):

    file_path = UPLOAD_DIR / filename

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return str(file_path)


# =========================================================
# SIMPLE TEXT RETRIEVAL
# =========================================================

def retrieve_documents(
    question: str,
    k: int = 5
):

    if not documents_store:

        print(
            "No documents uploaded."
        )

        return []

    question_words = set(
        question.lower().split()
    )

    scored_documents = []

    for document in documents_store:

        text = document.page_content.lower()

        score = 0

        for word in question_words:

            if len(word) < 2:
                continue

            if word in text:

                score += text.count(word)

        if score > 0:

            scored_documents.append(
                (
                    score,
                    document
                )
            )

    # -----------------------------------------------------
    # SORT BY RELEVANCE
    # -----------------------------------------------------

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # -----------------------------------------------------
    # TOP K
    # -----------------------------------------------------

    results = [
        document
        for score, document
        in scored_documents[:k]
    ]

    print(
        f"Retrieved {len(results)} documents "
        f"for question: {question}"
    )

    return results