resource "google_service_account" "iam" {
    account_id = "job-portal-sa"
    display_name = "Service account fot Job portal GKE"
}

resource "google_project_iam_member" "role" {
  for_each = toset([
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/artifactregistry.reader"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.iam.email}"
}