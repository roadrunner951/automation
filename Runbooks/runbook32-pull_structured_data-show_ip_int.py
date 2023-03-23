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
    version_result = task.run(task=send_command, command="show ip interface")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output() #use genie parse feature built by cisco.
    multicast_groups = task.host["facts"]["GigabitEthernet0/1"]["multicast_groups"]
    #print(multicast_groups)
    for multicast_ip in multicast_groups:
        #print(multicast_ip)
        if multicast_ip == "224.0.0.5": # multicast groups, 224.0.0.5-6 is ospf protocol
            rprint(f"{task.host}'s int G0/1 has OSPF enabled")

results = nr.run(task=pull_structured_data)
#print_result(results)
#ipdb.set_trace() # initiates ipdb debugger feature.  comment out after finding paths to info such as serial, uptime, etc via ipdb