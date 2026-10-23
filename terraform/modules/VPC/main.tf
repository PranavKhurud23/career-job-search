resource "google_compute_network" "carrer_vpc" {
    name = "carrer-vpc"
    auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "career_subnet" {
    name = "career-subnet"
    ip_cidr_range = "10.1.0.0/24"
    region = "asia-south1"
    network = google_compute_network.carrer_vpc.id
}