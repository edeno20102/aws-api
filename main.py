import boto3

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
AWS_REGION = "eu-west-1"

def create_aws_client(service, region):
    return boto3.client(
        service,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=region
    )

def list_services_and_details():
    """Lists AWS services and details for EC2 and RDS in all regions."""
    ec2_client = create_aws_client("ec2", AWS_REGION)
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        print(f"\nRegion: {region}")
        try:
            tagging_client = create_aws_client("resourcegroupstaggingapi", region)
            resources = tagging_client.get_resources()
            services = {res['ResourceARN'].split(':')[2] for res in resources['ResourceTagMappingList']}
            print(f"Services: {', '.join(services)}")

            #EC2
            if 'ec2' in services:
                ec2_client = create_aws_client("ec2", region)
                instances = ec2_client.describe_instances()
                for reservation in instances['Reservations']:
                    for instance in reservation['Instances']:
                        print(f"EC2 Instance: {instance['InstanceId']}, State: {instance['State']['Name']}")

            #RDS
            if 'rds' in services:
                rds_client = create_aws_client("rds", region)
                rds_instances = rds_client.describe_db_instances()
                for db in rds_instances['DBInstances']:
                    print(f"RDS Instance: {db['DBInstanceIdentifier']}, Status: {db['DBInstanceStatus']}")

        except Exception as e:
            print(f"Error fetching data for region {region}: {e}")

if __name__ == "__main__":
    list_services_and_details()
