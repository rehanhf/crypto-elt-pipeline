variable "minio_endpoint" {
  description = "MinIO Endpoint"
  type        = string
  default     = "localhost:9000"
}

variable "minio_user" {
  description = "MinIO Root User"
  type        = string
  default     = "admin" # Acceptable for local dev defaults
}

variable "minio_password" {
  description = "MinIO Root Password"
  type        = string
  sensitive   = true # Hides output in CLI
}

variable "postgres_password" {
  description = "Postgres User Password"
  type        = string
  sensitive   = true
}