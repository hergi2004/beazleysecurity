import boto3
import requests
import json
import argparse

# Initialize a Boto3 EC2 client that automatically uses the current AWS user role (credentials automatically resolved)
ec2_client = boto3.client('ec2')

def get_instance_metadata(public_ip):
    """
    Query the EC2 instance metadata via HTTP using the instance's public IP address.
    """
    metadata_url = f"http://{public_ip}/latest/meta-data/"
    
    # Retrieve all metadata keys
    try:
        response = requests.get(metadata_url)
        if response.status_code == 200:
            metadata = response.text.splitlines()
            result = {}
            for key in metadata:
                key_value = requests.get(metadata_url + key)
                result[key] = key_value.text
            return result
        else:
            return {"error": "Failed to retrieve metadata from instance"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error querying metadata: {str(e)}"}

def get_instance_public_ip(instance_id):
    """
    Retrieve the public IP address of an EC2 instance using the instance ID.
    """
    try:
        # Fetch instance details using Boto3
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        if public_ip:
            return public_ip
        else:
            return {"error": "Instance does not have a public IP address"}
    except Exception as e:
        return {"error": f"Error fetching public IP: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query EC2 instance metadata")
    parser.add_argument("--instance-id", help="The EC2 instance ID", type=str, required=True)
    parser.add_argument("--key", help="Specific metadata key to retrieve", type=str, required=False)

    args = parser.parse_args()

    # Get the public IP of the EC2 instance
    public_ip = get_instance_public_ip(args.instance_id)

    if 'error' in public_ip:
        print(json.dumps(public_ip, indent=4))
    else:
        # Query metadata for all keys or a specific key if provided
        if args.key:
            metadata = get_instance_metadata(public_ip)
            print(json.dumps({args.key: metadata.get(args.key)}, indent=4))
        else:
            metadata = get_instance_metadata(public_ip)
            print(json.dumps(metadata, indent=4))
