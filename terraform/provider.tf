terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0.0"
    }
  }
}

provider "google" {
    region = "asia-south1"
    project = "project-3abb875e-b867-4aaf-843"
}