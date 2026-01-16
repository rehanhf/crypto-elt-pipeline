terraform {
  required_providers {
    minio = {
      source = "aminueza/minio"
      version = ">= 1.0.0"
    }
    postgresql = {
      source = "cyrilgdn/postgresql"
      version = ">= 1.0.0"
    }
  }
}

# CONFIGURE PROVIDERS (Connect Terraform to your Docker containers)
provider "minio" {
  minio_server   = var.minio_endpoint
  minio_user     = var.minio_user
  minio_password = var.minio_password
  minio_ssl      = false
}

provider "postgresql" {
  host            = "localhost"
  port            = 5432
  database        = "warehouse"
  username        = "data_user"
  password        = var.postgres_password
  sslmode         = "disable"
}

# RESOURCE 1: Create the Data Lake Bucket
resource "minio_s3_bucket" "raw_data_bucket" {
  bucket = "raw-crypto-data"
  acl    = "public"
}

# RESOURCE 2: Create the Warehouse Schema
resource "postgresql_schema" "bronze_layer" {
  name  = "bronze"
  owner = "data_user"
}