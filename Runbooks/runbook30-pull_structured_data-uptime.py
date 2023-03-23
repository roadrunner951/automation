#sending show version command with structured data using gene parse feature.
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output() #use genie parse feature built by cisco.
    #print(task.host["facts"])#only used to view output in dictionary output.  Removed after task is complete.
    #uptime = task.host["facts"]["version"]["uptime"]# pulls uptime for each device using task.host (nr.inventory.hosts["R1"]["facts"])
    #print(f"{task.host} has an uptime of {uptime}")# prints output using f string format and task.host/uptime variables.


results = nr.run(task=pull_structured_data)
#print_result(results)
ipdb.set_trace() # initiates ipdb debugger feature.  comment out after finding paths to info such as serial, uptime, etc via ipdb