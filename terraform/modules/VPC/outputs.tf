output "vpc_id" {
    value = google_compute_network.carrer_vpc.id
    description = "ID for custome VPC"
}
output "subnet_id" {
    value = google_compute_subnetwork.career_subnet.id
    description = "ID for Subnet VPC"
}