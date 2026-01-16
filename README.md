# End-to-End Crypto Data Engineering Pipeline

## 📖 Overview
A containerized ELT pipeline that extracts cryptocurrency market data from the CoinGecko API, loads it into a Data Lake (MinIO), and transforms it within a Data Warehouse (Postgres) using dbt. The entire workflow is orchestrated by Apache Airflow.

## 🏗 Architecture


## 🛠 Tech Stack
*   **Language:** Python 3.10
*   **Orchestration:** Apache Airflow
*   **Containerization:** Docker & Docker Compose
*   **Transformation:** dbt (Data Build Tool)
*   **Data Lake:** MinIO (S3 Compatible)
*   **Data Warehouse:** PostgreSQL
*   **Visualization:** Metabase

## 🚀 How It Works
1.  **Extract:** Python script hits CoinGecko API for top 50 coins.
2.  **Load:** Data is saved as Parquet in MinIO (partitioned by date).
3.  **Staging:** A second script loads Parquet from MinIO to Postgres (`raw` schema), handling JSON serialization for nested API responses.
4.  **Transform:** dbt models clean the data, cast types, and materialize the `bronze` tables.
5.  **Schedule:** Airflow runs this DAG every hour.

## 🏃‍♂️ How to Run
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/rehanhf/crypto-elt.git
    cd crypto-elt
    ```
2.  **Set up environment:**
    Create a `.env` file (see `.env.example`).
3.  **Launch:**
    ```bash
    docker-compose up -d --build
    ```
4.  **Access UI:**
    *   Airflow: `localhost:8080` (user/pass: `admin`/`admin`)
    *   MinIO: `localhost:9001`
    *   Metabase: `localhost:3000`

## 📊 Dashboard Screenshot
