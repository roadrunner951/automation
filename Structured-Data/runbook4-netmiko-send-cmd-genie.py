#send command to parse data using genie parsers

import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def test_this(task):
    interfaces_result = task.run(task=netmiko_send_command, command_string="show ip interface", use_genie=True)
    task.host["facts"] = interfaces_result.result
    

results = nr.run(task=test_this)
print_result(results)
ipdb.set_trace()