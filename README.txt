 Purpose: This script is used to gather tag data from AWS ec2 instances
and compare them against canonical lists to ensure environmental consistency,
and report any deviations to the appropriate parties.
------------------------------------------------------------------------------------
 Author(s): John Reed, Nick Bitzer
 Python Version: 2.7.x

To execute script, initialize the python virtualenv by entering "source virtShell.sh",
Then execute the script "./aws_tag_check.py"

Script outputs tables to tagcheck.html, this is publish to a vhost on an aws instance,
and uses jenkins to excute the script daily, that overwrites the previous file, only if
a change is detected.

If you have created a new environment or product line, These tag values will need to be added to canonical.json so the script will not report your new instances as containing bad tags/values.

TODO:
# - add credential pass/fail
# - We should put in a check or something to make sure we're using the right account when running
#   prod account id: 703930589584
#   ecovate-ops id: 55050925507 maybe use a --test flag to switch to ops account.
# - 	Turn on debug with --debug flag
# - Prevent Table headers from printing if no bad data exists in a region


More to come...
