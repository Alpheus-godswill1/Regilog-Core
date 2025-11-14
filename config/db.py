import sqlite3
import os
from utils.logger import logger

db_dir = "instance/"
db_file = "user_registry.db" 

def get_db_connection():
    try:
        db_path = os.path.join(os.getcwd(), db_dir, db_file)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        return con
        logger.info("Database connection established.")     
    except Exception as e:
        return {"Error": str(e)}, 500
        logger.error(f"Database connection failed: {e}")   


def init_db():
    con = get_db_connection()
    if not con:
        logger.error("Failed to initialize database due to connection error.")
        return 
        

    try:
        cur = con.cursor()

        cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE, 
            password_hash TEXT NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        logger.info("Users table ensured in database.")
        con.commit()
        con.close
    except Exception as e:
        return {"Error": str(e)}, 500
        logger.error(f"Database initialization failed: {e}")
    

if __name__ == "__main__":
    from utils.logger import setup_logger
    setup_logger()
    init_db()
    logger.info("Database initialized.")