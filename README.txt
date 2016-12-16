 Purpose: This script is used to gather tag data from AWS ec2 instances
and compare them against canonical lists to ensure environmental consistency,
and report any deviations to the appropriate parties.
------------------------------------------------------------------------------------
 Author(s): John Reed, Nick Bitzer

To execute script, initialize the python virtualenv by entering "source virtShell.sh", Then execute the script "./aws_tag_check.py"

the script outputs the missing or incorrect EC2 tag data into html tables in index.html, this is published to ec2-54-175-234-75.compute-1.amazonaws.com (aws instance running apache2, vhost is tagcheck.conf).
A Jenkins job runs the script daily at 6am, that overwrites the previous file, if a change in data is detected.

If you have created a new environment or product line that differ from the connonical list, please see Seth Annibel to have that product/environment cannonical list updated.

TODO:
# - add credential pass/fail
# - We should put in a check or something to make sure we're using the right account when running
# - Prevent Table headers from printing if no bad data exists in a region
More to come...
