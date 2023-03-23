#sending show version command with structured data using gene parse feature.
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
#from rich import print as rprint#not needed after displaying cdp neighbor results
from nornir_scrapli.tasks import send_configs

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show cdp neighbor")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output() #use genie parse feature built by cisco.
    cdp_index = task.host["facts"]["cdp"]["index"]#same path as nr.inventory.hosts["R2"]["facts"]["cdp"]["index"]
    for num in cdp_index:
        local_intf = cdp_index[num]["local_interface"]
        remote_port = cdp_index[num]["port_id"]
        remote_device = cdp_index[num]["device_id"]
        #rprint(f"{task.host} {local_intf} is connected to {remote_device} {remote_port}")#display results of cdp neighbor as shown in notes.  comment out after building send command to automate descriptions to interfaces
        config_commands = [f"interface {local_intf}", f"description Connected to {remote_device} via its {remote_port}"]#sending configs to write descriptions to interfaces connecting to remote device
        task.run(task=send_configs, configs=config_commands)
    

results = nr.run(task=pull_structured_data)
print_result(results)
#ipdb.set_trace() # initiates ipdb debugger feature.  comment out after finding paths to info such as serial, uptime, etc via ipdb