#send configs from file
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def send_configs_test(task):
    task.run(task=send_configs_from_file, file="sendconfigcommands.txt") #'dry_run=True' omits send command listed and tests if connection is successful.  remove to send commands

results = nr.run(task=send_configs_test)
print_result(results)
