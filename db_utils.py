import sqlite3
from datetime import datetime

DB_PATH = 'database.db'

def initialize_db(db_path=DB_PATH):
    # Create the database file if it doesn't exist
    
    
    # Create connection and table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    conn.commit()
    conn.close()
    
    return db_path

def store_file_info(file_id, file_name, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO files (file_id, file_name, upload_date)
        VALUES (?, ?, ?)
    ''', (file_id, file_name, datetime.now()))
    
    conn.commit()
    conn.close()

def get_stored_files(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT file_id, file_name, upload_date 
        FROM files 
        WHERE status = 'active'
        ORDER BY upload_date DESC
    ''')
    files = cursor.fetchall()
    
    conn.close()
    
    return [
        {
            "file_id": file_id,
            "file_name": file_name,
            "upload_date": upload_date
        }
        for file_id, file_name, upload_date in files
    ]