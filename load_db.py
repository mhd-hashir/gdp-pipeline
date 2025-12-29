import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

def get_db_connection():
    # Fetch credentials from environment variables
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "password")
    db_port = os.getenv("DB_PORT", "5432")
    
    # URL encode user and password to handle special chars like '@'
    db_user_encoded = quote_plus(db_user)
    db_pass_encoded = quote_plus(db_pass)
    
    # Create SQLAlchemy engine
    # Format: postgresql://user:password@host:port/dbname
    connection_string = f"postgresql://{db_user_encoded}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)
    return engine

def load_data():
    csv_file = "gdp_history_2021_2025.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Run gdp_pipeline.py first.")
        return

    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Rename columns to be SQL-friendly (e.g., '2025' -> 'gdp_2025')
    # Current cols: Country, 2021, 2022, 2023, 2024, 2025
    rename_map = {col: f"gdp_{col}" for col in df.columns if col != 'Country'}
    rename_map['Country'] = 'country' # Lowercase for consistency
    df = df.rename(columns=rename_map)
    
    print("Columns renamed to:", df.columns.tolist())
    
    try:
        engine = get_db_connection()
        table_name = "gdp_data"
        
        print(f"Loading data into table '{table_name}'...")
        # if_exists='replace' drops the table if it exists and creates a new one
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"Successfully loaded {len(df)} rows into '{table_name}'.")
        
        # Verify
        result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", engine)
        print("Verification - Row count in DB:", result['count'].iloc[0])
        
    except Exception as e:
        print("Error connecting to database or loading data:")
        print(e)
        print("\nPlease ensure you have created a .env file with your database credentials.")
        print("Example .env content:\nDB_HOST=localhost\nDB_NAME=mydb\nDB_USER=postgres\nDB_PASS=mypassword")

if __name__ == "__main__":
    load_data()
