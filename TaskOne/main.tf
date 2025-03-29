provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Subnets
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
}

# Security Group
resource "aws_security_group" "eks_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EKS Cluster
resource "aws_eks_cluster" "eks" {
  name     = "my-eks-cluster"
  role_arn = aws_iam_role.eks.arn

  vpc_config {
    subnet_ids = [aws_subnet.public.id, aws_subnet.private.id]
  }
}

# EKS Node Group
resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks.name
  node_role_arn   = aws_iam_role.eks.arn
  subnet_ids      = [aws_subnet.public.id, aws_subnet.private.id]
  instance_types  = ["t3.medium"]
  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }
}

# Helm Charts for Services
resource "helm_release" "frontend" {
  name       = "frontend"
  repository = "https://charts.example.com"
  chart      = "frontend-chart"
  namespace  = "default"

  values = [
    <<EOF
replicaCount: 2
service:
  type: LoadBalancer
  port: 80
EOF
  ]
}

resource "helm_release" "backend" {
  name       = "backend"
  repository = "https://charts.example.com"
  chart      = "backend-chart"
  namespace  = "default"

  values = [
    <<EOF
replicaCount: 2
service:
  type: ClusterIP
  port: 8080
EOF
  ]
}

resource "helm_release" "database" {
  name       = "database"
  repository = "https://charts.example.com"
  chart      = "postgresql"
  namespace  = "default"

  values = [
    <<EOF
postgresqlUsername: "admin"
postgresqlPassword: "securepassword"
postgresqlDatabase: "appdb"
EOF
  ]
}
