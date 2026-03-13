# NeoStats: Virtual Server Monitoring & Performance Optimization Pipeline

## Project Overview
XYZ Corporation faces challenges in monitoring server performance and identifying resource bottlenecks across its distributed cloud infrastructure[cite: 2, 3]. This project provides an automated end-to-end data pipeline that ingests raw server logs, processes them securely, and visualizes health metrics to enable proactive issue resolution and optimized resource utilization[cite: 5, 6].


## Cloud Infrastructure Setup

To run this pipeline, the following Azure resources must be configured. Follow these steps to ensure the connection strings match the project requirements.

### **Step 1: Azure Data Lake Storage (ADLS) Gen2**

1. **Create a Storage Account**: Search for "Storage accounts" in the Azure Portal and create a new one.
2. **Enable Gen2**: Under the **Advanced** tab, ensure **"Enable hierarchical namespace"** is checked.
3. **Create Container**: Once deployed, go to **Containers** and create a new container named `raw-server-logs`.
4. **Get Credentials**: Go to **Access keys** and copy your **Connection string**. Paste this into your `.env` file as `AZURE_STORAGE_CONNECTION_STRING`.

### **Step 2: Azure SQL Database**

1. **Create SQL Server**: Search for "SQL servers" and create a new server. Use **SQL Authentication** and set an admin username and password.
2. **Configure Firewall**: Go to the server's **Networking** tab and click **"Add your client IPv4 address"** so your local machine can connect.
3. **Create Database**: Inside the server, create a database named `NeoStatsDB`.
4. **Get Connection Details**:
* **Server Name**: e.g., `your-server.database.windows.net`
* **Database Name**: `NeoStatsDB`
* **Username/Password**: The credentials you created in step 1.
* Update these in your `.env` file.



### **Step 3: Environment Configuration (`.env`)**

Create a file named `.env` in the root directory and populate it with the following keys. This ensures the Python scripts can authenticate without hardcoded credentials.

```text
# Azure Storage
AZURE_STORAGE_CONNECTION_STRING="your_connection_string_here"
CONTAINER_NAME="raw-server-logs"

# Azure SQL Database
SQL_SERVER="your-server.database.windows.net"
SQL_DATABASE="NeoStatsDB"
SQL_USERNAME="your_username"
SQL_PASSWORD="your_password"
SQL_DRIVER="ODBC Driver 18 for SQL Server"

# Security
ENCRYPTION_KEY="your_generated_fernet_key_here"

```

## Key Features & Requirements Met
* **Automated Ingestion**: Programmatic upload of raw CSV logs to Azure Data Lake Storage (ADLS) Gen2[cite: 9, 21].
* **Data Enrichment**: Dynamic assignment of `Instance_Size` (Small, Medium, Large) based on memory usage thresholds[cite: 14].
* **Advanced Security (Bonus)**: Implementation of AES-128 encryption to secure sensitive PII (Personally Identifiable Information) such as IP addresses and hostnames[cite: 23].
* **Metric Calculation**: Automated calculation of CPU utilization, memory usage, and total network traffic[cite: 13].
* **Interactive Analytics**: Two-page Power BI dashboard featuring server health trends, uptime statistics, and interactive slicers[cite: 16, 17, 30].

## Project Structure
```text
neostats_assignment/
├── data/                   # Local landing zone for raw and processed CSVs
├── src/                    # Modular Python scripts
│   ├── ingestion.py        # Handles Azure Data Lake uploads
│   ├── transformation.py   # Cleans data, enriches metadata, and encrypts PII
│   └── load.py             # Loads transformed data into Azure SQL
├── main_pipeline.py        # MASTER AUTOMATION SCRIPT
├── .env                    # Secure credential storage (SQL, Azure keys)
├── requirements.txt        # Necessary Python libraries
└── dashboard/              # Power BI (.pbix) report file

```

## How to Run the Project

### 1. Prerequisites

* Python 3.9+ installed.
* An active Azure Subscription with a configured **Data Lake Storage Gen2** and **Azure SQL Database**.
* **ODBC Driver 18 for SQL Server** installed on your machine.

### 2. Setup Environment

1. Clone this repository or extract the project folder.
2. Open your terminal and create a virtual environment:
```bash
python -m venv neostats_env
source neostats_env/bin/activate  # On Windows: neostats_env\Scripts\activate

```


3. Install dependencies:
```bash
pip install -r requirements.txt

```


4. Configure the `.env` file with your Azure credentials.

5. Generate Key: 
 ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
 ```
Copy the output of this command and paste it into the ENCRYPTION_KEY field in your .env file.

### 3. Execute the Pipeline

Place your raw log file (of any name) into the `data/` folder. Then, simply run the master automation script:

```bash
python main_pipeline.py

```

**This script will automatically:**

1. Upload the raw file to Azure Data Lake.


2. Clean and transform the data (including PII encryption).


3. Load the processed dataset into the Azure SQL Database `ServerPerformanceMetrics` table.



### 4. View the Dashboard

1. Open `dashboard/NeoStats_Server_Monitoring.pbix` in **Power BI Desktop**.
2. Click **Refresh** on the Home ribbon to pull the newly processed data from your Azure SQL Database.


3. Use the **OS Type** and **Server Location** slicers to explore resource utilization and reliability trends.

## Data Schemas

### 1. Raw Input Schema (Source)

| Column Name | Data Type | Description |
| --- | --- | --- |
| **Server_ID** | String | Unique identifier for the virtual server. |
| **Hostname** | String | Human-readable network name. |
| **IP_Address** | String | Plain-text server IP address (PII). |
| **OS_Type** | String | Operating System version. |
| **Server_Location** | String | Geographical data center location. |
| **CPU_Utilization (%)** | Decimal | Raw CPU usage percentage. |
| **Memory_Usage (%)** | Decimal | Raw RAM usage percentage. |
| **Disk_IO (%)** | Decimal | Raw Disk I/O percentage. |
| **Network_Traffic_In** | Decimal | Raw inbound traffic (MB/s). |
| **Network_Traffic_Out** | Decimal | Raw outbound traffic (MB/s). |
| **Uptime (Hours)** | Decimal | Total active hours. |
| **Downtime (Hours)** | Decimal | Total inactive hours. |
| **Admin_Name** | String | Plain-text administrator name (PII). |
| **Admin_Email** | String | Plain-text administrator email (PII). |
| **Admin_Phone** | String | Plain-text administrator phone (PII). |
| **Log_Timestamp** | String | Original log timestamp string. |

### 2. Processed & Enriched Schema (Target)

| Column Name | Data Type | Type | Value-Add / Logic |
| --- | --- | --- | --- |
| **Server_ID** | String | Metadata | Standardized GUID. |
| **Hostname** | String | Metadata | Retained for identification. |
| **IP_Address** | **Encrypted** | Secured | **AES-128 Encryption** applied (PII Handling). |
| **OS_Type** | String | Category | Cleaned categorical data. |
| **Server_Location** | String | Category | Cleaned categorical data. |
| **CPU_Utilization (%)** | Decimal | Metric | Validated numerical metric. |
| **Memory_Usage (%)** | Decimal | Metric | Validated numerical metric. |
| **Disk_IO (%)** | Decimal | Metric | Validated numerical metric. |
| **Uptime (Hours)** | Decimal | Reliability | Used for availability analysis. |
| **Downtime (Hours)** | Decimal | Reliability | Used for availability analysis. |
| **Admin_Name** | **Encrypted** | Secured | **AES-128 Encryption** applied (PII Handling). |
| **Admin_Email** | **Encrypted** | Secured | **AES-128 Encryption** applied (PII Handling). |
| **Admin_Phone** | **Encrypted** | Secured | **AES-128 Encryption** applied (PII Handling). |
| **Log_Timestamp** | DateTime | Time | Normalized to standard DateTime format. |
| **Instance_Size** | String | **Enriched** | **Logic:** Categorized (Small/Med/Large) based on Memory. |
| **Total_Network_Traffic** | Decimal | **Calculated** | **Logic:** Combined Inbound + Outbound (MB/s). |

---

**Developed by:** Sohil S Philip - Ph:7683039177 - Email : sohilphilip137@gmail.com

**For:** Team NeoStats Case Study Submission 


