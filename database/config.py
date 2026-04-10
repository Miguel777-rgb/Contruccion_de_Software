# config.py
import os
from dotenv import load_dotenv

# Load variables from .env into process environment
load_dotenv()

# ========== MYSQL CONFIGURATION (PRIMARY) ==========
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "task_db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

# Build a SQLAlchemy-compatible connection URI using PyMySQL driver
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ========== POSTGRESQL CONFIGURATION (REPLICA) ==========
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_NAME = os.getenv("PG_NAME", "task_db_pg")

# PostgreSQL connection URI for replication
POSTGRESQL_DATABASE_URI = (
    f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"
)

# Enable replication to PostgreSQL
ENABLE_REPLICATION = os.getenv("ENABLE_REPLICATION", "true").lower() == "true"

# Disable event system overhead we don't use
SQLALCHEMY_TRACK_MODIFICATIONS = False
