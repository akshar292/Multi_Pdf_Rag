import shutil
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# =========================================================
# ENV
# =========================================================

load_dotenv()


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CHROMA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# EMBEDDING MODEL
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# TEXT SPLITTER
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# =========================================================
# VECTOR DATABASE
# =========================================================

vectorstore = Chroma(
    collection_name="multi_pdf_rag",
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
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

        text = page.extract_text()

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
    # ADD TO CHROMA
    # -----------------------------------------------------

    if chunks:

        vectorstore.add_documents(
            chunks
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
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    question: str,
    k: int = 5
):

    try:

        documents = vectorstore.similarity_search(
            question,
            k=k
        )

        return documents

    except Exception as e:

        print(
            "Retrieval error:",
            e
        )

        return []