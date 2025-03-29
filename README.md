# Task one: 3-Tier Architecture

The 3-tier architecture below will use Terraform as a tool to deploy the services. Let's break it down:


1. Presentation Layer (Frontend)

The frontend is a deployment, service and ingress (k8s load balancer) deployed on eks with hel

2. Application Layer (Backend)

the backend is a deployment with a service deployed on Kubernetes Deployment (EKS) with services for API requests.

3. Data Layer (Database)

Uses Amazon RDS (PostgreSQL/MySQL) or DynamoDB for managed databases.

# Task two: query the meta data of an AWS EC2 instance

to perform this taks we will use the aws CDK called boto3 client which is a python library for aws. The script will assume the aws role of your current local laptop

1. Get Public IP:

The get_instance_public_ip function uses Boto3 to query for the EC2 instance's public IP using the instance ID.

2. Fetch Metadata:

The get_instance_metadata function sends HTTP requests to the EC2 instance metadata endpoint (http://<instance_public_ip>/latest/meta-data/) to retrieve all metadata or a specific metadata key.

3. Argument Parsing:

You can specify an EC2 instance-id and optionally a specific metadata key you want to retrieve.

4. Install dependencies

```
pip install -r requirements.txt
```

5. run the script from your local laptop:

```
python3 query_ec2_metadata.py --instance-id i-0abcd1234efgh5678
```

6. Retreive a specific key called ami-id

```
python3 query_ec2_metadata.py --instance-id i-0abcd1234efgh5678 --key ami-id
```
# Task three: nested object

A function get_nested_values, which takes two arguments: obj and key, will split the key into a list with a split () method, then iteratge through each key and update obj to the corresponding nested values. Then if all keys are found it returns the values corresponding to the last key

```
python nested.py
```