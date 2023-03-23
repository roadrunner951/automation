from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

target = input("Enter the mac address that you wish to find: ")
#print(f"The target is {target}")#verify if above input command works.  Comment out after test is successful.

def pull_info(task):

    interface_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = interface_result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for interface in interfaces:
        #print(interface)#only to check interfaces results.  Remove after done.
        mac_addr = interfaces[interface]["mac_address"]
        #print(mac_addr)#only to check mac address results. Remove after done.
        if target == mac_addr:
            #print(mac_addr)#check if mac is located.
            intf = interface
            print_info(task, intf)

def print_info(task, intf):

    print(f"MAC ADDRESS: {target} is present on {task.host}'s {intf}")
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]
            print(f"Connected to {dev_id} on its interface {port_id}")



nr.run(task=pull_info)
import ipdb
ipdb.set_trace()
