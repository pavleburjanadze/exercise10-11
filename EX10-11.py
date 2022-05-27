import boto3

ec2_client = boto3.client("ec2")

vpc_id = "vpc-030ebd0e749ba6a09"
subnet_id = "subnet-04a7fa1165b7cc38f"

def create_security_group(name, description):
   response = ec2_client.create_security_group(
       Description=description,
       GroupName=name,
       VpcId=vpc_id
   )
   group_id = response.get("GroupId")
   print(group_id)
   return group_id


def add_ssh_access_sg(group_id, ip_address):
   ip_address = f"{ip_address}/32"

   response = ec2_client.authorize_security_group_ingress(
       CidrIp=ip_address,
       FromPort=22,
       GroupId=group_id,
       IpProtocol='tcp',
       ToPort=22,
   )

def add_http_access_sg(group_id, ip_address):
   ip_address = "0.0.0.0/16"

   response = ec2_client.authorize_security_group_ingress(
       CidrIp=ip_address,
       FromPort=80,
       GroupId=group_id,
       IpProtocol='http',
       ToPort=80,
   )

def create_key_pair():
   response = ec2_client.create_key_pair(
       KeyName="btu",
       KeyType="rsa"
   )
   key_id = response.get("KeyPairId")
   with open("btu.pem", "w") as file:
       file.write(response.get("KeyMaterial"))
   print(key_id)

def run_ec2(group_id, subnet_id):
   response = ec2_client.run_instances(
       BlockDeviceMappings=[
           {
               "DeviceName": "/dev/sdh",
               "Ebs": {"DeleteOnTermination": True,
                       "VolumeSize": 10,
                       "VolumeType": "gp1",
                       "Encrypted": False},
           },
       ],
       ImageId="ami-015c25ad8763b2f11",
       InstanceType="t2.micro",
       KeyName="btu",
       MaxCount=1,
       MinCount=1,
       Monitoring={"Enabled": True},
       UserData="#!/bin/bash"
                sudo apt update -y && sudo apt upgrade -y
                sudo apt install nginx -y
                sudo apt install nginx nginx-full -y
                sudo apt install nginx-extras -y
                systemctl status nginx > info.txt"",
       InstanceInitiatedShutdownBehavior="stop",
       NetworkInterfaces=[
           {
               "AssociatePublicIpAddress": True,
               "DeleteOnTermination": True,
               "Groups": [
                   group_id,
               ],
               "DeviceIndex": 0,
               "SubnetId": subnet_id,
           },
       ],
   )
   for instance in response.get("Instances"):
       instance_id = instance.get("InstanceId")
       print("InstanceId - ", instance_id)
   return None


def enable_auto_public_ips(subnet_id, action):
   new_state = True if action == "enable" else False
   response = ec2_client.modify_subnet_attribute(
       MapPublicIpOnLaunch={
           "Value": new_state
       },
       SubnetId=subnet_id
   )
   print("Public IP association state changed to", new_state)



def main():
    create_security_group("HTTP", "Allow from all IP")
    create_key_pair()
    add_http_access_sg("212.58.120.152")
    run_ec2(group_id, subnet_id)
    enable_auto_public_ips(subnet_id, action)



if __name__ == "__main__":
   main()








