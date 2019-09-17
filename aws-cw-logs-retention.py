import boto3
import csv

session = boto3.session.Session()

cw_client = session.client('logs', region_name='us-east-1')
stscli = session.client(service_name='sts')

# fetch AWS account id
Account_ID = stscli.get_caller_identity()['Account']

# Declaring Boolean variables
dryRun = False

# Generating the CSV file to report all the logGroups which have retention not equal to 180 days.

csv_header = ['S_No','Account_ID','logGroup_Name','creation_Time','retention_InDays']
fo=open("cwlogs_retention_compliance_report.csv","w")
csv_w=csv.writer(fo)
csv_w.writerow(csv_header)
S_no = 1

for i in cw_client.describe_log_groups()['logGroups']:
    if i['retentionInDays'] > 180:
        log_grp_name = i['logGroupName']
        creation_Time = i['creationTime']
        retention_InDays = i['retentionInDays']

        csv_w.writerow([S_no,Account_ID,log_grp_name,creation_Time,retention_InDays])
        S_no = S_no+1
# Changing the loggroup retention to 180 days.
        if dryRun == False:
            try:
                print(f"CW loggroup {log_grp_name} retention is {retention_InDays} and not in compliance so changing it to 180 days :")
                response = cw_client.put_retention_policy(logGroupName=log_grp_name, retentionInDays=180)
            except Exception as e:
                raise

fo.close()
