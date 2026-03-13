import pandas as pd
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# 1. Load environment variables
load_dotenv()

def get_encryption_cipher():
    """Retrieves the encryption key and creates a cipher."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not found in .env file!")
    return Fernet(key.encode())

def encrypt_column(df, column_name, cipher):
    """Encrypts a specific column in the DataFrame."""
    # Convert data to string, encode to bytes, encrypt, and decode back to string for storage
    df[column_name] = df[column_name].astype(str).apply(
        lambda x: cipher.encrypt(x.encode()).decode() if pd.notnull(x) else x
    )
    return df

def assign_instance_size(memory_usage):
    """Business logic to categorize server sizes based on memory usage."""
    if memory_usage < 30.0:
        return 'Small'
    elif memory_usage < 70.0:
        return 'Medium'
    else:
        return 'Large'

if __name__ == "__main__":
    print("--- Starting Phase 4: Data Transformation ---")
    
    # Define dynamic paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_file_path = os.path.join(base_dir, "data", "Sample_Data_Ingestion.csv")
    processed_file_path = os.path.join(base_dir, "data", "Processed_Server_Logs.csv")

    try:
        # Step A: Read the raw data
        print("Reading raw data...")
        df = pd.read_csv(raw_file_path)

        # Step B: Data Cleansing (Standardize the timestamp)
        print("Standardizing date formats...")
        df['Log_Timestamp'] = pd.to_datetime(df['Log_Timestamp'], format='mixed')

        # Step C: Data Enrichment (Add Instance Size)
        print("Enriching data with Instance Size...")
        df['Instance_Size'] = df['Memory_Usage (%)'].apply(assign_instance_size)

        # Step D: Metric Calculation (Total Network Traffic)
        print("Calculating Total Network Traffic...")
        df['Total_Network_Traffic (MB/s)'] = df['Network_Traffic_In (MB/s)'] + df['Network_Traffic_Out (MB/s)']

        # Step E: PII Encryption (Secure sensitive columns)
        print("Encrypting sensitive PII data...")
        cipher = get_encryption_cipher()
        pii_columns = ['IP_Address', 'Admin_Name', 'Admin_Email', 'Admin_Phone']
        
        for col in pii_columns:
            df = encrypt_column(df, col, cipher)

        # Step F: Save the processed data
        print("Saving transformed data...")
        df.to_csv(processed_file_path, index=False)
        
        print(f"--- Phase 4 Complete! Processed file saved to: {processed_file_path} ---")

    except Exception as e:
        print(f"--- Phase 4 Failed: {e} ---")