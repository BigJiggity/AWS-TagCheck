#!/usr/bin/env python

"""
 Purpose: This script is used to gather tag data from AWS ec2 instances and compare them against canonical lists to ensure environmental consistency,
 and report any deviations to the appropriate parties.
 Author(s): John Reed, Nick Bitzer
 Python Version: 2.7.x
"""
# Imports
from aws import AWS
from aws import *
import json
import argparse
import logging
from prettytable import PrettyTable
import boto.ec2
import sys

# Log generator
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
LOG = logging.getLogger("root.aws_tag_check")
LOG.setLevel(logging.INFO)

# Regions we don't have access to with our current account
BAD_REGIONS = ["cn-north-1", "us-gov-west-1"]

# json files for import
CON_FILE = 'canonical.json'
HTML_FILE = 'index.html'

# Print Webpage headers
with open(HTML_FILE, 'w') as f:
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<body>\n")
    f.write("<h1> AWS Tag Check Report</h1>\n")
    f.write("<p> Please look at the following systems listed in the tables in each region."
                     "All systems must have Environment and Product tags, with the values found"
                     "<a href=""https://confluence.ecovate.com/display/EN/AWS+Tags""> here.</a></p>")
    f.write("<p> Please update the systems through the AWS console if created manually,"
                     "or update your Terraform code where needed.\n")
f.close()

def get_canonical_data(filename):
    """
    Reads data from a json file
    :returns dict
    """

    #LOG.info("Reading in file {}".format(filename))
    with open(filename) as f:
        return json.load(f)

def main():
    NAMES = []
    ENVIRONMENTS = []
    PRODUCTS = []
    FINAL = []

    # Read in canonical data set for tags.
    canonical_data = get_canonical_data(CON_FILE)

    # Now that we have the canonical data, organize it into difference lists for comparisons later.
    for data in canonical_data['Environment']:
        ENVIRONMENTS.append(data)
    for data in canonical_data['Product']:
        PRODUCTS.append(data)

    # Global Variables
    returncode = 1
    cvalue = 0
    rvalue = 0

    # Gather Region data and connect
    regions = boto.ec2.regions()
    for r in regions:
        if r.name in BAD_REGIONS:
            continue
        conn = AWS(r.name)
        conn = conn.connect_to_ec2()

        # Retrieve instance data
        reservations = conn.get_all_instances()
        if reservations:
            LOG.info("Instances found in region {}!".format(r.name))
            with open(HTML_FILE, 'a') as f:

                # Create table for bad data
                table = PrettyTable(['Instance ID', 'Server Name', 'Environment', 'Product'])
                table.hrules = True
                table.format = True

                # Iterate through AWS instances, tag data
                for res in reservations:
                    for inst in res.instances:
                        for t in inst.tags:

                            #Checks if Tag key exists
                            if "Name" in inst.tags and not None:
                                v_name = inst.tags['Name']
                            else:
                                v_name = "missing name"
                            if "Product" in inst.tags and not None:
                                a_prod = inst.tags['Product']
                            else:
                                a_prod = "missing product"
                            if "Environment" in inst.tags and not None:
                                a_env = inst.tags['Environment']
                            else:
                                a_env = "missing environment"
                                break

                        # Check for bad tag values, and print those in table
                        bad_env = check_data(a_env, ENVIRONMENTS)
                        bad_prod = check_data(a_prod, PRODUCTS)
                        if bad_prod != None and bad_env != None:
                            table.add_row([inst.id, v_name, a_env, a_prod])
                        else:
                            break

                # Prints all table data and page formatting
                f.write("<h2> Region {}</h2>".format(r.name))
                f.write(table.get_html_string())
            CODECHECK = ['bad_tag1, bad_tag2, bad_env, bad_prod']
            for c in CODECHECK:
                if c == None:
                    cvalue = 0
                else:
                    cvalue = 1
        rvalue += returncode
    else:
        LOG.info("There are no instances in region {}".format(r.name))

    # Finish writing the closing HTML tags
    with open(HTML_FILE, 'a') as f:
        f.write("</body> \n")
        f.write("</html> \n")
        f.close()

    # Checks for and sets returncode value for Jenkins notificaitons
    if rvalue == 0:
        returncode = 0
        sys.exit(returncode)
    else:
        sys.exit(returncode)


if __name__ == '__main__':
    main()
