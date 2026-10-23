variable "project_id" {
    type = string
    description = "The GCP project id"
}
variable "region" {
    type = string
    default = "asia-south1"
    description = "Region for vpc and subnet"
}