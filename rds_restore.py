#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_restore.py
Author:         Adeel Ahmad
Description:    Python Script to restore from RDS Backup
"""

from __future__ import absolute_import, \
        division, print_function, unicode_literals

__version__ = "0.1"

import os
from botocore.exceptions import ClientError
import boto3

RDS = boto3.client('rds')
INSTANCEID = os.environ.get('DBINSTANCEID')


def query_db_cluster(instanceid):
    """
    Querying whether DB is Clustered or not
    """
    try:
        db_instance = RDS.describe_db_instances(
            DBInstanceIdentifier=instanceid
            )
        return db_instance['DBInstances'][0]['DBClusterIdentifier']
    except KeyError:
        return False


def restore(instanceid, newid):
    """
    This command will restore RDS DB from latest snapshot.
    """
    if query_db_cluster(instanceid):
        cluster_id = query_db_cluster(instanceid)
        try:
            response = RDS.restore_db_cluster_to_point_in_time(
                DBClusterIdentifier=newid,
                SourceDBClusterIdentifier=cluster_id,
                UseLatestRestorableTime=True
                )
            return response['DBCluster'][0]['Status']
        except ClientError as error:
            print(error)
    else:
        try:
            response = RDS.restore_db_instance_to_point_in_time(
                SourceDBInstanceIdentifier=instanceid,
                TargetDBInstanceIdentifier=newid,
                UseLatestRestorableTime=True
                )
            return response['DBInstance'][0]['DBInstanceStatus']
        except ClientError as error:
            print(error)


if __name__ == "__main__":
    main(INSTANCEID)
    import doctest
    doctest.testmod()
