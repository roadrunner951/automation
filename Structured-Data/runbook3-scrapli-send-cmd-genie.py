#send command to parse data using genie parsers

import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.functions import print_structured_result#alternative to using print_result command
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def test_this(task):
    interfaces_result = task.run(task=send_command, command="show ip interface")
    #task.host["facts"] = interfaces_result.scrapli_response.genie_parse_output()

results = nr.run(task=test_this)
#print_result(results)
print_structured_result(results, parser="textfsm")#option: parser="textfsm" instead of using genie
#ipdb.set_trace()