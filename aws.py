"""
Class file for AWS API interaction (boto)
"""

import boto
import boto.ec2
import logging


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
LOG = logging.getLogger("root.foreman")
LOG.setLevel(logging.INFO)

__all__ = ['check_data',]

class AWS(object):
    def __init__(self, region):
        self.log = logging.getLogger("root.aws.AWS")
        self.region = region

    def connect_to_ec2(self):
        """
        Connect to ec2 for a given region.
        :returns ec2 object
        """
        return (boto.ec2.connect_to_region(self.region,
                 aws_access_key_id = 'AKIAIAWHGR3NN2T6C5PQ',
                 aws_secret_access_key = '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'))

""" Helper functions """
def check_data(item, values):
    """
    Check is a given string exists in a given list. Matches case!
    :param item string to be checked
    :param values list to check string against
    :returns string if it exists, else pass
    """
    if item not in values or item != item:
        return item
    else:
        pass
