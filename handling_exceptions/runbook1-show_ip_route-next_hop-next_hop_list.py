import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def get_routing_info(task):
    show_result = task.run(task=send_command, command="show ip route")
    task.host['facts'] = show_result.scrapli_response.genie_parse_output()
    routes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for key in routes:
        next_hop_list = routes[key]['next_hop']['next_hop_list']
        rprint(f"{task.host} NEXT HOP INFO {next_hop_list}")

results = nr.run(task=get_routing_info)
print_result(results)#uncomment this to see error
import ipdb#uncomment to use ipdb
ipdb.set_trace()#uncomment to debug error code