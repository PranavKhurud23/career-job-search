variable cluster_name {
    type = string
    description = "Define clustername"
}
variable vpc_name {
    type = string
    description = "Define VPC Name"
}
variable subnet_name {
    type = string
    description = "Define subnet name"
}
variable region {
    type = string
    default = "asia-south1"
    description = "Region"
}
variable service_account {
    type =  string 
    description = "IAM SA for Node"
}