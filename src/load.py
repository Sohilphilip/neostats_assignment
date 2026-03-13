import pandas as pd
import os
import urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Load environment variables
load_dotenv()

def load_data_to_azure_sql():
    """Reads the processed CSV and loads it into Azure SQL Database."""
    
    # 2. Retrieve SQL credentials from the .env file
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    
    if not all([server, database, username, password]):
        print("ERROR: Missing SQL credentials in the .env file.")
        return False

    # 3. URL-encode the password (crucial if your password has special characters like @ or !)
    encoded_password = urllib.parse.quote_plus(password)
    
    # 4. Define the ODBC Driver (Driver 17 is the standard for Azure SQL on Windows)
    driver = "ODBC Driver 18 for SQL Server"
    
    # Construct the SQLAlchemy connection string
    connection_string = f"mssql+pyodbc://{username}:{encoded_password}@{server}:1433/{database}?driver={driver.replace(' ', '+')}"
    
    try:
        print("Connecting to Azure SQL Database...")
        # Create the database engine (fast_executemany speeds up the upload process)
        engine = create_engine(connection_string, fast_executemany=True)
        
        # 5. Define paths and read the processed data
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        processed_file_path = os.path.join(base_dir, "data", "Processed_Server_Logs.csv")
        
        print(f"Reading processed data from {processed_file_path}...")
        df = pd.read_csv(processed_file_path)
        
        # 6. Push the data to Azure SQL
        table_name = "ServerPerformanceMetrics"
        print(f"Loading {len(df)} rows into the '{table_name}' table...")
        
        # if_exists='replace' creates the table if it doesn't exist, and overwrites it if it does
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print("Upload successful!")
        return True

    except Exception as e:
        print(f"Failed to load data to Azure SQL: {e}")
        print("\n--- TROUBLESHOOTING TIP ---")
        print("If you see an 'ODBC Driver' error, change the 'driver' variable on line 28")
        print("from 'ODBC Driver 18 for SQL Server' to 'ODBC Driver 18 for SQL Server' or just 'SQL Server'.")
        return False

if __name__ == "__main__":
    print("--- Starting Phase 5: Data Loading ---")
    
    success = load_data_to_azure_sql()
    
    if success:
        print("--- Phase 5 Complete! Your pipeline is fully functional! ---")
    else:
        print("--- Phase 5 Failed. ---")