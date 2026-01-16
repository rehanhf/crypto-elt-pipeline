FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Postgres adapter
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python libraries
# boto3/pyarrow = MinIO access
# sqlalchemy/psycopg2 = Postgres access
RUN pip install pandas requests boto3 pyarrow fastparquet sqlalchemy psycopg2-binary

# Copy scripts
COPY src/etl_script.py .
COPY src/loader.py . 

# We will override the CMD in docker-compose
CMD ["python", "etl_script.py"]