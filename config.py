import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

class Config:
    """Application configuration management."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-scam-detector-2025")

    # API Keys for AI Services (stored securely in env vars)
    AI_API_KEY = os.environ.get("AI_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GROQ_API_KEY")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "openai").lower()  # e.g., 'openai', 'gemini', 'groq'
    AI_API_URL = os.environ.get("AI_API_URL")

    # Upload limits & rules
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    # Tesseract OCR executable path override if needed
    TESSERACT_CMD = os.environ.get("TESSERACT_CMD", None)
