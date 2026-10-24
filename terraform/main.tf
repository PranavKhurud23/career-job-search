module "vpc" {
    source = "./modules/VPC"
    project_id = "project-3abb875e-b867-4aaf-843"
}

module "iam" {
    source = "./modules/IAM"
    project_id = "project-3abb875e-b867-4aaf-843"
}

module "gke" {
    source = "./modules/GKE"
    cluster_name = "job-portal"
    vpc_name = module.vpc.vpc_name
    subnet_name = module.vpc.subnet_name
    service_account = module.iam.service_account_mail
}