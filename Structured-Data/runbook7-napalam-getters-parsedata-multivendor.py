
import os
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=["get_facts"])
    task.host["facts"] = interfaces_result.result
    uptime = task.host["facts"]["get_facts"]["uptime"]
    model = task.host["facts"]["get_facts"]["vendor"]
    if model == "Juniper":
        rprint(f"{task.host} is a [green]Juniper[/green] device (uptime {uptime})")
        
    elif model == "Cisco":
        rprint(f"{task.host} is a [yellow]Cisco[/yellow] device (uptime {uptime})")

results = nr.run(task=pull_interfaces_info)
#print_result(results)

