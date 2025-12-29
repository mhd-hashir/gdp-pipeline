import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine for the configured PostgreSQL database.
    Reads credentials from .env file.
    """
    # Fetch credentials
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "password")
    db_port = os.getenv("DB_PORT", "5432")
    
    # URL encode user and password to safely handle special characters
    db_user_encoded = quote_plus(db_user)
    db_pass_encoded = quote_plus(db_pass)
    
    # Construct connection string
    # Format: postgresql://user:password@host:port/dbname
    connection_string = f"postgresql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise e

if __name__ == "__main__":
    # Test connection
    try:
        eng = get_db_engine()
        with eng.connect() as conn:
            print("Successfully connected to the database!")
    except Exception as e:
        print("Connection failed.")
