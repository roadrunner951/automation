#using getpass module for multi password management when automating.
#using sys argv

import sys
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
north_password = getpass.getpass(prompt="Enter the North group password: ")
south_password = getpass.getpass(prompt="Enter the South group password: ")
r7_password = getpass.getpass(prompt="Enter R7's password: ")

nr.inventory.groups["north"].password = north_password
nr.inventory.groups["south"].password = south_password
nr.inventory.hosts['R7'].password = r7_password
nr.inventory.defaults.username = sys.argv[1] #command will be "python3 runbook27-sysargv.py <username>"

def credential_test(task):
    task.run(task=send_command, command="show ip interface brief")

results = nr.run(task=credential_test)
print_result(results)