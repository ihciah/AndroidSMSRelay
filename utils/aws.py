# -*-coding: utf-8 -*-
__author__ = 'ihciah'

from datetime import datetime
from dateutil.tz import tzutc

def get_used_bandwidth():
    import boto3
    now = datetime.utcnow()
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='NetworkOut',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'i-068fb997b5721188c'
            },
        ],
        StartTime=datetime(now.year, now.month, 1, 0, 0, tzinfo=tzutc()),
        EndTime=datetime(now.year, now.month, now.day, 23, 59, tzinfo=tzutc()),
        Period=31*24*3600,
        Statistics=[
            'Sum',
        ],
        #Unit='Gigabytes'
    )
    return response['Datapoints'][0]['Sum']

if __name__ == "__main__":
    used = get_used_bandwidth()
    print "%.2f GB" % (used/(1000**3))
