terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
   credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "dataproc_bucket" {
    name          = var.bucket
    location      = "US"
    storage_class = "STANDARD"
}

resource "google_dataproc_cluster" "spark-streaming-cluster" {
    name        = "football-spark-streaming-cluster"
    project     = var.project
    region      = var.region
    

    cluster_config {

      staging_bucket = google_storage_bucket.dataproc_bucket.name
        master_config {
            num_instances = 1
            machine_type  = "n1-standard-2"
        }
        worker_config {
            num_instances = 2
            machine_type  = "n1-standard-2"
        }
    }
  
   
}

resource "google_bigquery_dataset" "stg_dataset" {
  dataset_id                 = var.stg_bq_dataset
  project                    = var.project
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id                 = var.prod_bq_dataset
  project                    = var.project
  location                   = var.region
  delete_contents_on_destroy = true
}