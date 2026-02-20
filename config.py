from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Get the absolute path to the .env file in the project root
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


# Project Root
ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "NutriFit AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "nutrifit_db"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # Gemini
    GEMINI_API_KEY: Optional[str] = None
    
    # Tesseract
    TESSERACT_CMD: Optional[str] = None
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = str(ROOT_DIR / "uploads")
    ALLOWED_EXTENSIONS: list = ["pdf", "png", "jpg", "jpeg"]
    
    # Model Paths
    DIABETES_MODEL_PATH: str = str(ROOT_DIR / "models" / "diabetes_model.pkl")
    HYPERTENSION_MODEL_PATH: str = str(ROOT_DIR / "models" / "hypertension_model.pkl")
    THYROID_MODEL_PATH: str = str(ROOT_DIR / "models" / "thyroid_model.pkl")
    OBESITY_MODEL_PATH: str = str(ROOT_DIR / "models" / "obesity_model.pkl")
    FOOD_RECOGNITION_MODEL_PATH: str = str(ROOT_DIR / "models" / "food_recognition_model.h5")
    
    # Vector Database
    FAISS_INDEX_PATH: str = str(ROOT_DIR / "data" / "faiss_index")
    NUTRITION_DATA_PATH: str = str(ROOT_DIR / "data" / "nutrition_dataset.csv")
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = True


settings = Settings()
