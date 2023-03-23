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
    testvar = task.host["cdpinfo"]    
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]
            

    ver_result = task.run(task=send_command, command="show version")
    task.host["verinfo"] = ver_result.scrapli_response.genie_parse_output()
    version = task.host["verinfo"]["version"]
    serial_num = version["chassis_sn"]
    oper_sys = version["os"]
    uptime = version["uptime"]
    version_short = version["version_short"]
    print(f"DEVICE MGMT IP: {task.host.hostname}")
    print(f"DEVICE SERIAL NUMBER: {serial_num}")
    print(f"DEVICE OPERATING SYSTEM: {oper_sys}")
    print(f"DEVICE UPTIME: {uptime}")
    print(f"DEVICE VESION: {version_short}")
    print(f"Connected to {port_id} on {dev_id}")


nr.run(task=pull_info)
#import ipdb
#ipdb.set_trace()
