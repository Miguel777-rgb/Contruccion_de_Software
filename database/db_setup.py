# db_setup.py
import sys
import os
from sqlalchemy import create_engine, text

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from back.app import create_app
from database.models import db
from database import config

# First, create the database if it doesn't exist
# Connect without specifying a database
db_url_without_db = config.SQLALCHEMY_DATABASE_URI.rsplit('/', 1)[0]
engine = create_engine(db_url_without_db)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}"))
    conn.commit()
    print(f"✅ Database '{config.DB_NAME}' ensured to exist.")

# Now create the app and tables
app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created (or already exist).")
