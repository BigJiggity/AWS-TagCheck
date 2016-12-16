"""
Class file for AWS API interaction (boto)
"""

import logging
import boto
import boto.ec2

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
LOG = logging.getLogger("root.foreman")
LOG.setLevel(logging.INFO)

__all__ = ['check_data']


class AWS(object):
    """
    Connection handling for AWS.
    """

    def __init__(self, region):
        """
        default constructor for AWS class
        """
        self.log = logging.getLogger("root.aws.AWS")
        self.region = region

    def connect_to_ec2(self):
        """
        :connect to ec2 for a given region.
        returns ec2 object
        key id/secret is for aws account aws_srvc,this is a service account that doesn't have a login/password
        and is used exclusively for execution of this script to retrieve instance tag data.
        """
        return(boto.ec2.connect_to_region(self.region, aws_access_key_id='',
                                          aws_secret_access_key=''))


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
