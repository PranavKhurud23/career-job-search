module "vpc" {
    source = "./modules/VPC"
    project_id = "8237"
}

module "iam" {
    source = "./modules/IAM"
    project_id = "8237"
}

module "gke" {
    source = "./modules/GKE"
    cluster_name = "job-portal"
    vpc_name = module.vpc.vpc_name
    subnet_name = module.vpc.subnet_name
    service_account = module.iam.service_account_mail
}