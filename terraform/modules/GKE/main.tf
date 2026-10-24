resource "google_container_cluster" "my_cluster" {
    name = "job-portal"
    location = "asia-south1"
    remove_default_node_pool = true
    network = var.vpc_name
    subnetwork = var.subnet_name
}
resource "google_container_node_pool" "primary_node" {
    name = "${var.cluster_name}-node-pool"
    location = var.region
    cluster = google_container_cluster.my_cluster.name
}