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
            print(f"{task.host}'s {interface} has the mac address {mac_addr}")
            
nr.run(task=pull_info)
#import ipdb
#ipdb.set_trace()
