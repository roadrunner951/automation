#send command to parse data using genie parsers

import os
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=["get_facts"])
    task.host["facts"] = interfaces_result.result

results = nr.run(task=pull_interfaces_info)
print_result(results)
ipdb.set_trace()
