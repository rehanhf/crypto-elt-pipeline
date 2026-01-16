FROM apache/airflow:2.7.1-python3.10

# Switch to root to install system dependencies
USER root
RUN apt-get update && \
    apt-get install -y git libpq-dev gcc && \
    apt-get clean

# Switch back to airflow user to install python packages
USER airflow

# Install your pipeline dependencies
RUN pip install --no-cache-dir \
    pandas \
    requests \
    boto3 \
    pyarrow \
    fastparquet \
    sqlalchemy \
    psycopg2-binary \
    dbt-postgres