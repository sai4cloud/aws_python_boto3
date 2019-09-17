import boto3
import csv

'''
Session object created if we run this script out of AWS resources. 
If we run this from AWS EC2 instance just have IAM role attached to it
with required policies attached and remove the session object
'''

session = boto3.session.Session()

ec2res = session.resource(service_name='ec2', region_name='us-east-1')
ec2cli = session.client(service_name='ec2', region_name='us-east-1')
stscli = session.client(service_name='sts')

# fetch AWS account id
Account_ID = stscli.get_caller_identity()['Account']

## Getting list of all regions

region_list = [region['RegionName'] for region in ec2cli.describe_regions()['Regions']]
#print(region_list)

# CSV file initialization

csv_header = ['S_No','Account_ID','Region','VPC_Id','InstanceID','InstanceType','State','Public_IP','Private_IP','Ena_Support','Architecture','Image_Id','Iam_profile','Key_name','Key_pair','Launch_time','Monitoring','Network_Interfaces','Platform','Hyperviosr']
fo=open("ec2_inventory.csv","w")
csv_w=csv.writer(fo)
csv_w.writerow(csv_header)
S_no = 1

'''
From all Regions, we get list of all Instances regardless of status of Instance. 
Different variables has used to fetch required results if at all we need any other
values, all we need is just assign variable in below for loop. 

We used Resource object since we get all details required, if not we can use
ec2 client object as well but again we need to change the variables accordingly 
as per describe_instances 
'''

for region in region_list:
    ec2_region_resource = session.resource('ec2', region_name=region)
    all_instances = ec2_region_resource.instances.all()
    for instance in all_instances:

        ins_iam = instance.iam_instance_profile
        ins_keyname = instance.key_name
        ins_keypair= instance.key_pair
        ins_launchtime = instance.launch_time
        ins_monitoring = instance.monitoring['State']
        ins_networkinterfaces = instance.network_interfaces
        ins_platform = instance.platform
        ins_securitygroup = instance.security_groups[0]['GroupName']
        ins_state = instance.state['Name']
        ins_instance_id = instance.instance_id
        ins_image_id = instance.image_id
        ins_instance_type = instance.instance_type
        ins_image = instance.image.id
        ins_hyp = instance.hypervisor
        ins_ena_support = instance.ena_support
        ins_architecture = instance.architecture
        ins_subnet = instance.subnet.id
        ins_vpc_id = instance.vpc_id
        ins_public_ip_address = instance.public_ip_address
        ins_private_ip_address = instance.private_ip_address

        # writing CSV row as it loops
        csv_w.writerow([S_no,Account_ID,region,ins_vpc_id,ins_instance_id,ins_instance_type,ins_state,ins_public_ip_address,ins_private_ip_address,ins_ena_support,ins_architecture,ins_image_id,ins_iam,ins_keyname,ins_keypair,ins_launchtime,ins_monitoring,ins_networkinterfaces,ins_platform,ins_hyp])

        S_no = S_no+1

fo.close()