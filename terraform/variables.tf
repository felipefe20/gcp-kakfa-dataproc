variable "region" {
  description = "The region to deploy the resources in."
  default     = "us-east1"
}

variable "bucket" {
  description = "Staging bucket name"
  default     = "in-game-football-data"
}

variable "network" {
  description = "Network name"
}

variable "zone" {
  description = "The zone to deploy the resources in."
  default     = "us-east1"
}

variable "credentials" {
  description = "The path to the Google Cloud credentials file."
  default     = "mycreds.json"
}

variable "project" {
  description = "Google Cloud project ID"
  default     = "resounding-hope-414923"
}


variable "stg_bq_dataset" {
  description = "staging BigQuery dataset ID"
  type        = string
}

variable "prod_bq_dataset" {
  description = "Production BigQuery dataset ID"
  type        = string
}