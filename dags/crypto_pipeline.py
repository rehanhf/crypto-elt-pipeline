from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Import scripts
from etl_script import extract_and_load
from loader import load_to_warehouse

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'crypto_elt_pipeline',
    default_args=default_args,
    description='A simple ELT pipeline',
    schedule_interval=timedelta(hours=1), # Runs every hour
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # TASK 1: Extract (API -> MinIO)
    t1_extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_and_load
    )

    # TASK 2: Load (MinIO -> Postgres Raw)
    t2_load = PythonOperator(
        task_id='load_data',
        python_callable=load_to_warehouse
    )

    # TASK 3: Transform (dbt)
    t3_transform = BashOperator(
        task_id='dbt_transform',
        bash_command="""
            rm -rf /tmp/dbt_run && \
            cp -R /opt/airflow/dbt/crypto_dbt /tmp/dbt_run && \
            
            echo "Overwriting sources.yml..." && \
            echo "version: 2" > /tmp/dbt_run/models/staging/sources.yml && \
            echo "sources:" >> /tmp/dbt_run/models/staging/sources.yml && \
            echo "  - name: raw_layer" >> /tmp/dbt_run/models/staging/sources.yml && \
            echo "    database: warehouse" >> /tmp/dbt_run/models/staging/sources.yml && \
            echo "    schema: raw" >> /tmp/dbt_run/models/staging/sources.yml && \
            echo "    tables:" >> /tmp/dbt_run/models/staging/sources.yml && \
            echo "      - name: source_coingecko" >> /tmp/dbt_run/models/staging/sources.yml && \
            
            cd /tmp/dbt_run && \
            dbt run --profiles-dir .
        """
    )