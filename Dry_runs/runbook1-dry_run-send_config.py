import os
from nornir import InitNornir
from nornir.core import task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def nuggets(task):
    task.run(task=napalm_configure, filename="napalm-config.txt", dry_run=True)

results = nr.run(task=nuggets)
print_result(results)