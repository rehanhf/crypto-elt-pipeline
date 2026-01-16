FROM python:3.9-slim

# Set working directory
WORKDIR /usr/app/dbt

# Install dbt-postgres
RUN pip install dbt-postgres

# Copy the entire dbt project into the container
COPY ./crypto_dbt .

# Set the profile directory
ENV DBT_PROFILES_DIR=.

# Default command
CMD ["dbt", "run"]