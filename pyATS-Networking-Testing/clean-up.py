import json
from rich import print as rprint 
from nornir import InitNornir
from nornir_scrapli.tasks import send_command, send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def get_cdp(task):
    interfaces_list = []#lsit of unconnected interfaces including mgmt/loopback0 that configs will be removed and shutdown.
    interfaces_result = task.run(task=send_command, command="show ip interface brief | json")
    task.host["interfaces_facts"] = json.loads(interfaces_result.result)
    interfaces = task.host["interfaces_facts"]["TABLE_interface"]["ROw_interface"]
    for interface in interfaces:
        intf = interface["interface"]
        #print(intf)#test
        if intf not in ("mgmt0", "loopback0"):#excluding mgmt/loopback0 from interface to iterate through.
            interfaces_list.append(intf)
    #rprint(interfaces_list)#test

    cdp_result = task.run(task=send_command, command="show cdp neighbor | json")
    task.host["cdp_facts"] = json.loads(cdp_result.result)#debug after this line to locate required keys.
    connections = task.host["cdp_facts"]["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]
    for device in connections:
        platform = device["platform_id"]
        if platform == "N9K-9000v":
            local_intf = device["intf_id"]
            interfaces_list.remove(local_intf)
    #rprint(f"{task.host}")#test
    #rprint(f"{interfaces_list}")#test
    #print("\n\n")#test
    clean_interfaces(task, interfaces_list)

def clean_interfaces(task, interfaces_list):
    for interface in interfaces_list:
        task.run(task=send_configs, configs=[f"interface {interface}", "switchport", "shutdown", "description SHUTDOWN"])



nr.run(task=get_cdp)
#results = nr.run(task=get_cdp)#set variable
#print_result(results)#display results
import ipdb
ipdb.set_trace()
