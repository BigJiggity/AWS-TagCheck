#!/usr/bin/env python

"""
Purpose: This script is used to gather tag data from AWS ec2 instances and
compare them against canonical lists to ensure environmental consistency,
and report any deviations to the appropriate parties.
Author(s): John Reed, Nick Bitzer
 """

# Imports
import json
import logging
import sys
import datetime
from prettytable import PrettyTable
from aws import AWS
from aws import *
import boto.ec2


# Log generator
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
LOG = logging.getLogger("root.aws_tag_check")
LOG.setLevel(logging.INFO)

# Regions we don't have access to with our current account
BAD_REGIONS = ["cn-north-1", "us-gov-west-1"]

# file definitions: json file that contains canonical list of Environments and Products
# html file contains the output of missing or invalid tag data
CON_FILE = 'canonical.json'
HTML_FILE = 'index.html'

# Print Webpage headers
with open(HTML_FILE, 'w') as html_open:
    html_open.write('''
<!DOCTYPE html>
<html>
<body>
    <h1><u>AWS Tag Check Report</u></h1>
    ''')
    html_open.write("<h2><u>{}</u></h2>".format(datetime.date.today()))
    html_open.write('''
<pre>
*******************************************************************************
* Please look at the following systems listed in the tables in each region.   *
* All systems must have Environment and Product tags. If there is a "+" in    *
* field it means that the value is good.                                      *
*                                                                             *
* The list of values can be found below:                                      *
* <a href=https://confluence.ecovate.com/display/EN/AWS+Tags>canonical List</a>                                                              *
*                                                                             *
* Please update the systems through the AWS console if created manually,      *
* or update your Terraform code where needed with the correct tags/values.    *
* If there is a value that you feel needs to be added to the canonical list   *
* please contact Seth Annabel at <a href=mailto:seth.annabel@readytalk.com>seth.annabel@readytalk.com</a>                   *
*******************************************************************************
</pre>
    <hr></hr>

        ''')


def get_canonical_data(filename):
    """
     Reads data from a json file
     :returns dict
    """
    with open(filename) as canonical_file:
        return json.load(canonical_file)


CANONICAL_DATA = get_canonical_data(CON_FILE)
# Now that we have the canonical data, organize it into difference lists for comparisons later.
CANONICAL_ENVIRONMENTS = [data for data in CANONICAL_DATA['Environment']]
CANONICAL_PRODUCTS = [data for data in CANONICAL_DATA['Product']]


def main():
    """
    Main data execution.
    """

    # Variable to set exit code
    error_count = 0

    # Gather Region data and connect
    regions = boto.ec2.regions()
    for region in regions:
        if region.name in BAD_REGIONS:
            continue
        conn = AWS(region.name)
        connect = conn.connect_to_ec2()

        # Create table for bad data
        table = PrettyTable(['Instance ID', 'Server Name', 'Environment', 'Product'])
        table.hrules = True
        table.format = True

        # Retrieve instance data
        reservations = connect.get_all_instances()
        if reservations:
            LOG.info("Instances found in region {}!".format(region.name))
            with open(HTML_FILE, 'a') as html:

                # Iterate through AWS instances, tag data
                for res in reservations:
                    for inst in res.instances:
                        for tag in inst.tags:

                            # Checks if Tag key exists
                            if "Name" in inst.tags and not None:
                                amazon_name = inst.tags['Name']
                            else:
                                amazon_name = "missing name"
                            if "Product" in inst.tags and not None:
                                amazon_product = inst.tags['Product']
                            else:
                                amazon_product = "missing product"
                            if "Environment" in inst.tags and not None:
                                amazon_environment = inst.tags['Environment']
                            else:
                                amazon_environment = "missing environment"
                                continue

                        # Check for bad tag values, and print those in table
                        bad_environment = check_data(amazon_environment, CANONICAL_ENVIRONMENTS)
                        bad_product = check_data(amazon_product, CANONICAL_PRODUCTS)
                        if bad_product is not None:
                            table.add_row([inst.id, amazon_name, "+", amazon_product])
                            error_count += 1
                        elif bad_environment is not None:
                            table.add_row([inst.id, amazon_name, amazon_environment, "+"])
                            error_count += 1
                        else:
                            break

                # Print region name and coresponding data
                html.write("<h2> Region {}</h2>".format(region.name))
                html.write(table.get_html_string())
        else:
            LOG.info("There are no instances in region {}".format(region.name))

    # Prints closing html tags
    with open(HTML_FILE, 'a') as html_close:
        html_close.write('''
</body>
</html>
            ''')
        html_close.close()

    sys.exit(error_count)

if __name__ == '__main__':
    main()
