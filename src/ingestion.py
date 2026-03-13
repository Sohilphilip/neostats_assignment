import pandas as pd
import os
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient  # <-- THIS WAS THE MISSING LINE

# Load the environment variables from your .env file
load_dotenv()

def read_local_data(file_path):
    """Reads the local CSV file into a pandas DataFrame safely."""
    print(f"Attempting to read data from: {file_path}")
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        print(f"Successfully read {len(df)} rows of data.")
        return df
    except FileNotFoundError:
        print(f"ERROR: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return None

def upload_to_datalake(local_file_path, file_name_in_azure):
    """Uploads a local file to the Azure Data Lake file system."""
    
    # 1. Retrieve credentials from the .env file
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    file_system_name = os.getenv("DATALAKE_CONTAINER_NAME") # Container = File System in ADLS Gen2

    if not connect_str or not file_system_name:
        print("ERROR: Azure credentials not found. Check your .env file.")
        return False

    try:
        print("Connecting to Azure Data Lake...")
        # 2. Create the DataLakeServiceClient using the connection string
        service_client = DataLakeServiceClient.from_connection_string(conn_str=connect_str)
        
        # 3. Get a client to interact with the specific file system (container)
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)
        
        # 4. Get a client to interact with the specific file we are creating
        file_client = file_system_client.get_file_client(file_name_in_azure)

        # 5. Open the local file and upload it
        print(f"Uploading '{local_file_path}' to file system '{file_system_name}'...")
        with open(local_file_path, "rb") as data:
            # We use create_file() first, then append_data, then flush_data in ADLS Gen2
            # However, upload_data() is a convenient wrapper for small/medium files
            file_client.upload_data(data, overwrite=True) 
            
        print("Upload successful!")
        return True

    except Exception as e:
        print(f"Failed to upload to Azure: {e}")
        return False
    
if __name__ == "__main__":
    # Use a relative path to go up one folder, then into the 'data' folder
    # This works dynamically on any computer!
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_csv_file = os.path.join(base_dir, "data", "Sample_Data_Ingestion.csv")
    
    azure_destination_name = "raw_server_logs_landing.csv"

    print("--- Starting Phase 3: Data Ingestion ---")
    
    # Step 1: Validate the local file can be read
    df = read_local_data(local_csv_file)
    
    if df is not None:
        # Step 2: If the file is readable, upload it to Azure
        success = upload_to_datalake(local_csv_file, azure_destination_name)
        
        if success:
            print("--- Phase 3 Complete! ---")
        else:
            print("--- Phase 3 Failed during upload. ---")
    else:
        print("--- Phase 3 Failed: Could not read local data. ---")