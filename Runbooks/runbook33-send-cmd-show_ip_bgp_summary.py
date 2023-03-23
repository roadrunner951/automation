#sending show version command with structured data using gene parse feature.
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
from rich import print as rprint#formating module

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show ip bgp summary")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output() #use genie parse feature built by cisco.
    '''neighbors = task.host["facts"]["vrf"]["default"]["neighbor"]
    for key in neighbors:
        updown = neighbors[key]["address_family"][""]["up_down"]
        rprint(f"{task.host} neighbor {key} updown value is {updown}")
'''
results = nr.run(task=pull_structured_data)
#print_result(results)
ipdb.set_trace() # initiates ipdb debugger feature.  comment out after finding paths to info such as serial, uptime, etc via ipdb