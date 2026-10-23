output "vpc_name" {
    value = google_compute_network.carrer_vpc.name
    description = "ID for custome VPC"
}
output "subnet_name" {
    value = google_compute_subnetwork.career_subnet.name
    description = "ID for Subnet VPC"
}