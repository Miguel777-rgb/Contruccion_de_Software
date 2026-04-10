#!/usr/bin/env python3
"""Migration script to update users table schema"""

import sys
import os
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import config

# Connect to database
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

with engine.connect() as conn:
    try:
        # Get current columns
        result = conn.execute(text("SHOW COLUMNS FROM users"))
        columns = {row[0] for row in result.fetchall()}
        
        # Drop foreign key to allow drops
        try:
            conn.execute(text("ALTER TABLE tasks DROP FOREIGN KEY fk_tasks_user_id"))
            conn.commit()
            print("✅ Dropped old foreign key")
        except:
            print("⚠️ Foreign key didn't exist or already dropped")
        
        # Drop columns if they exist
        if 'email' in columns:
            conn.execute(text("ALTER TABLE users DROP COLUMN email"))
            conn.commit()
            print("✅ Dropped email column")
        
        if 'username' in columns:
            conn.execute(text("ALTER TABLE users DROP COLUMN username"))
            conn.commit()
            print("✅ Dropped username column")
        
        if 'password_hash' in columns:
            conn.execute(text("ALTER TABLE users DROP COLUMN password_hash"))
            conn.commit()
            print("✅ Dropped password_hash column")
        
        # Refresh columns
        result = conn.execute(text("SHOW COLUMNS FROM users"))
        columns = {row[0] for row in result.fetchall()}
        
        # Add new columns if they don't exist
        if 'name' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(80) NOT NULL DEFAULT 'User' AFTER id"))
            conn.commit()
            print("✅ Added name column")
        
        if 'lastname' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN lastname VARCHAR(80) AFTER name"))
            conn.commit()
            print("✅ Added lastname column")
        
        if 'city' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN city VARCHAR(100) AFTER lastname"))
            conn.commit()
            print("✅ Added city column")
        
        if 'country' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN country VARCHAR(100) AFTER city"))
            conn.commit()
            print("✅ Added country column")
        
        if 'postal_code' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN postal_code VARCHAR(10) AFTER country"))
            conn.commit()
            print("✅ Added postal_code column")
        
        # Recreate foreign key
        conn.execute(text("""
            ALTER TABLE tasks 
            ADD CONSTRAINT fk_tasks_user_id 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        """))
        conn.commit()
        print("✅ Recreated foreign key")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        sys.exit(1)

print("\n✅ Schema migration completed successfully!")
