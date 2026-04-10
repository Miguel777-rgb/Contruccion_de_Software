#!/usr/bin/env python3
"""
Database Replication Manager: MySQL <-> PostgreSQL
Sync tables between MySQL (primary) and PostgreSQL (replica)
"""

import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey, inspect, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import config

class DatabaseReplicator:
    """Manage replication between MySQL and PostgreSQL"""
    
    def __init__(self):
        # MySQL (primary)
        self.mysql_engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.mysql_metadata = MetaData()
        
        # PostgreSQL (replica)
        self.pg_engine = create_engine(config.POSTGRESQL_DATABASE_URI, echo=False)
        self.pg_metadata = MetaData()
        
        self.mysql_session = sessionmaker(bind=self.mysql_engine)()
        self.pg_session = sessionmaker(bind=self.pg_engine)()
    
    def create_pg_tables(self):
        """Create replica tables in PostgreSQL with same structure as MySQL"""
        try:
            print("\n📋 Creating tables in PostgreSQL...")
            
            # Reflect MySQL tables
            self.mysql_metadata.reflect(bind=self.mysql_engine)
            
            # Create equivalent tables in PostgreSQL
            with self.pg_engine.connect() as conn:
                # Drop existing tables if they exist
                conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE;"))
                conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
                conn.commit()
                
                # Create users table
                conn.execute(text("""
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(80) NOT NULL,
                        lastname VARCHAR(80),
                        city VARCHAR(100),
                        country VARCHAR(100),
                        postal_code VARCHAR(10),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP NULL
                    );
                """))
                print("✅ Users table created")
                
                # Create tasks table
                conn.execute(text("""
                    CREATE TABLE tasks (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                        content VARCHAR(200) NOT NULL,
                        done BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP NULL
                    );
                """))
                print("✅ Tasks table created")
                
                # Create indexes for performance
                conn.execute(text("CREATE INDEX idx_tasks_user_id ON tasks(user_id);"))
                conn.execute(text("CREATE INDEX idx_tasks_deleted_at ON tasks(deleted_at);"))
                conn.execute(text("CREATE INDEX idx_users_deleted_at ON users(deleted_at);"))
                print("✅ Indexes created")
                
                conn.commit()
            
            print("✅ PostgreSQL tables created successfully!\n")
            return True
            
        except Exception as e:
            print(f"❌ Error creating PostgreSQL tables: {e}")
            return False
    
    def sync_mysql_to_pg(self):
        """Sync data from MySQL to PostgreSQL"""
        try:
            print("\n🔄 Syncing MySQL → PostgreSQL...")
            
            with self.pg_engine.connect() as pg_conn:
                # Truncate tables
                pg_conn.execute(text("TRUNCATE TABLE tasks CASCADE;"))
                pg_conn.execute(text("TRUNCATE TABLE users CASCADE;"))
                pg_conn.commit()
                
                # Copy users
                with self.mysql_engine.connect() as mysql_conn:
                    users_result = mysql_conn.execute(text("SELECT * FROM users;"))
                    users_list = users_result.fetchall()
                    for user in users_list:
                        pg_conn.execute(text(
                            """INSERT INTO users 
                            (id, name, lastname, city, country, postal_code, created_at, updated_at, deleted_at)
                            VALUES (:id, :name, :lastname, :city, :country, :postal_code, :created_at, :updated_at, :deleted_at)"""
                        ), {
                            "id": user[0], "name": user[1], "lastname": user[2], "city": user[3],
                            "country": user[4], "postal_code": user[5], "created_at": user[6], "updated_at": user[7], "deleted_at": user[8]
                        })
                    pg_conn.commit()
                    print(f"✅ Users synced ({len(users_list)} rows)")
                    
                    # Copy tasks
                    tasks_result = mysql_conn.execute(text("SELECT * FROM tasks;"))
                    tasks_list = tasks_result.fetchall()
                    for task in tasks_list:
                        pg_conn.execute(text(
                            """INSERT INTO tasks 
                            (id, user_id, content, done, created_at, updated_at, deleted_at)
                            VALUES (:id, :user_id, :content, :done, :created_at, :updated_at, :deleted_at)"""
                        ), {
                            "id": task[0], "user_id": task[1], "content": task[2], "done": bool(task[3]),
                            "created_at": task[4], "updated_at": task[5], "deleted_at": task[6]
                        })
                    pg_conn.commit()
                    print(f"✅ Tasks synced ({len(tasks_list)} rows)")
            
            print("✅ MySQL → PostgreSQL sync completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Error syncing MySQL to PostgreSQL: {e}")
            return False
    
    def sync_pg_to_mysql(self):
        """Sync data from PostgreSQL to MySQL (if needed)"""
        try:
            print("\n🔄 Syncing PostgreSQL → MySQL...")
            
            with self.mysql_engine.connect() as mysql_conn:
                # Truncate tables
                mysql_conn.execute(text("TRUNCATE TABLE tasks;"))
                mysql_conn.execute(text("TRUNCATE TABLE users;"))
                mysql_conn.commit()
                
                # Copy users
                with self.pg_engine.connect() as pg_conn:
                    users_result = pg_conn.execute(text("SELECT * FROM users;"))
                    users_list = users_result.fetchall()
                    for user in users_list:
                        mysql_conn.execute(text(
                            """INSERT INTO users 
                            (id, name, lastname, city, country, postal_code, created_at, updated_at, deleted_at)
                            VALUES (:id, :name, :lastname, :city, :country, :postal_code, :created_at, :updated_at, :deleted_at)"""
                        ), {
                            "id": user[0], "name": user[1], "lastname": user[2], "city": user[3],
                            "country": user[4], "postal_code": user[5], "created_at": user[6], "updated_at": user[7], "deleted_at": user[8]
                        })
                    mysql_conn.commit()
                    print(f"✅ Users synced ({len(users_list)} rows)")
                    
                    # Copy tasks
                    tasks_result = pg_conn.execute(text("SELECT * FROM tasks;"))
                    tasks_list = tasks_result.fetchall()
                    for task in tasks_list:
                        mysql_conn.execute(text(
                            """INSERT INTO tasks 
                            (id, user_id, content, done, created_at, updated_at, deleted_at)
                            VALUES (:id, :user_id, :content, :done, :created_at, :updated_at, :deleted_at)"""
                        ), {
                            "id": task[0], "user_id": task[1], "content": task[2], "done": bool(task[3]),
                            "created_at": task[4], "updated_at": task[5], "deleted_at": task[6]
                        })
                    mysql_conn.commit()
                    print(f"✅ Tasks synced ({len(tasks_list)} rows)")
            
            print("✅ PostgreSQL → MySQL sync completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Error syncing PostgreSQL to MySQL: {e}")
            return False
    
    def verify_sync(self):
        """Verify data is consistent between both databases"""
        try:
            print("\n🔍 Verifying data consistency...\n")
            
            with self.mysql_engine.connect() as mysql_conn:
                mysql_users = mysql_conn.execute(text("SELECT COUNT(*) FROM users;")).scalar()
                mysql_tasks = mysql_conn.execute(text("SELECT COUNT(*) FROM tasks;")).scalar()
            
            with self.pg_engine.connect() as pg_conn:
                pg_users = pg_conn.execute(text("SELECT COUNT(*) FROM users;")).scalar()
                pg_tasks = pg_conn.execute(text("SELECT COUNT(*) FROM tasks;")).scalar()
            
            print(f"MySQL Users: {mysql_users} | PostgreSQL Users: {pg_users}")
            print(f"MySQL Tasks: {mysql_tasks} | PostgreSQL Tasks: {pg_tasks}")
            
            if mysql_users == pg_users and mysql_tasks == pg_tasks:
                print("\n✅ Databases are in SYNC!\n")
                return True
            else:
                print("\n⚠️ Databases are OUT OF SYNC!\n")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying sync: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        self.mysql_session.close()
        self.pg_session.close()


def main():
    print("=" * 60)
    print("🗄️  DATABASE REPLICATION MANAGER (MySQL ↔ PostgreSQL)")
    print("=" * 60)
    
    replicator = DatabaseReplicator()
    
    try:
        # Test connections
        print("\n🔗 Testing connections...")
        with replicator.mysql_engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        print("✅ MySQL connected")
        
        with replicator.pg_engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        print("✅ PostgreSQL connected")
        
        # Create PostgreSQL tables
        if not replicator.create_pg_tables():
            return 1
        
        # Sync data
        if not replicator.sync_mysql_to_pg():
            return 1
        
        # Verify
        if not replicator.verify_sync():
            return 1
        
        print("=" * 60)
        print("✅ REPLICATION SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📌 Next Steps:")
        print("1. Update .env with PostgreSQL credentials if needed")
        print("2. Update database models to support both engines")
        print("3. Run: python database/db_replicator.py (to keep in sync)")
        print("\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    finally:
        replicator.close()


if __name__ == "__main__":
    sys.exit(main())
