import os

API_TOKEN_EXPIRATION_HOURS = int(os.getenv("API_TOKEN_EXPIRATION_HOURS", "12"))
API_TOKEN_SECRET = os.getenv("API_TOKEN_SECRET", "your-secret-key")

DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "construction_management")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_CONNECTION_STR = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
