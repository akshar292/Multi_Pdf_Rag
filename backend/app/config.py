import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Please add it to the .env file."
    )

CHROMA_DIR = "./chroma_db"
UPLOAD_DIR = "./data/uploads"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5