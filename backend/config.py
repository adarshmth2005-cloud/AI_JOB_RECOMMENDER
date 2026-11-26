
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# Load .env from backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))

    if not DB_USER or DB_PASSWORD is None or not DB_NAME:
        raise RuntimeError(
            "Database configuration missing. Check environment variables."
        )

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    # Aiven requires SSL
    ca_path = os.path.join(BASE_DIR, "ca.pem")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": ca_path
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
