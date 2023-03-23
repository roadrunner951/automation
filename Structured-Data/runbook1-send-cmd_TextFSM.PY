#sending commands using templates/TextFSM
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def test_this(task):
    #task.run(task=send_command, command="show clock")
    clock_results = task.run(task=send_command, command="show interface description")
    structured_output = clock_results.scrapli_response.textfsm_parse_output()
    print(structured_output)

results = nr.run(task=test_this)
#print_result(results)