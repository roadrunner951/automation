#sending commands using templates/TextFSM

import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command#using netmiko
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def test_this(task):
    clock_results = task.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
#    structured_result = clock_results.result
#    print(structured_result)

results = nr.run(task=test_this)
print_result(results)