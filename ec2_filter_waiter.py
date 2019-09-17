import boto3
import pprint

session=boto3.session.Session()

ec2_res=session.resource(service_name='ec2',region_name='us-east-1')
ec2_cli=session.client(service_name='ec2',region_name='us-east-1')

# iterable variables

instance_iterator = ec2_res.instances.all()
instance_filter = ec2_res.instances.filter

# filter variables
ins_tag= {'Name' : 'tag-key', 'Values' : ['Owner']}

# Declaring instance list

Ins_list = []

for ins in instance_filter(Filters=[ins_tag]):
    #Ins_list = ins.id
    Ins_list.append(ins.id)
print(Ins_list)

# Polls EC2.Client.describe_instances() every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.
#waiter = ec2_cli.get_waiter('instance_running')
waiter = ec2_cli.get_waiter('instance_stopped')
#ec2_cli.start_instances(InstanceIds=Ins_list)
ec2_cli.stop_instances(InstanceIds=Ins_list)
waiter.wait(InstanceIds=Ins_list)