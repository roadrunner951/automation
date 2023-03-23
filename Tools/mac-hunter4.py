import os#allows executing linux commands from python scripts
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")#initialize InitNornir

target_list = []

CLEAR = "clear"#linux command to clear the screen
os.system(CLEAR)#excute clear command

target = input("Enter the mac address that you wish to find: ")
#print(f"The target is {target}")#verify if above input command works.  Comment out after test is successful.

def pull_info(task):

    interface_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = interface_result.scrapli_response.genie_parse_output()#binding to "facts" and running genie parser.
    interfaces = task.host["facts"]
    for interface in interfaces:
        try:#error handling
            mac_addr = interfaces[interface]["mac_address"]
            if target == mac_addr:
                target_list.append(mac_addr)
                intf = interface
                print_info(task, intf)
        except KeyError:#Error handling
            pass#even there's error, script will continue

def print_info(task, intf):
    rprint("\n[green]*** TARGET IDENTIFIED ***[/green]")
    print(f"MAC ADDRESS: {target} is present on {task.host}'s {intf}")
    rprint("\n[cyan]GENERATING DETAILS...[/cyan]")
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
    dev_id = ""#for downed interfaces or interfaces with no show cdp neighbor results.
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]
            

    ver_result = task.run(task=send_command, command="show version")
    task.host["verinfo"] = ver_result.scrapli_response.genie_parse_output()#binding to "verinfo" and running genie parser.
    version = task.host["verinfo"]["version"]
    serial_num = version["chassis_sn"]
    oper_sys = version["os"]
    uptime = version["uptime"]
    version_short = version["version_short"]
    print(f"DEVICE MGMT IP: {task.host.hostname}")
    print(f"DEVICE SERIAL NUMBER: {serial_num}")
    print(f"DEVICE OPERATING SYSTEM: {oper_sys}")
    print(f"DEVICE UPTIME: {uptime}")
    print(f"DEVICE VERSION: {version_short}")
    if dev_id:
        rprint("[cyan]REMOTE CONNECTION DETAILS...[/cyan]")
        print(f"Connected to {port_id} on {dev_id}")


nr.run(task=pull_info)
#results = nr.run(task=pull_info)
#print_result(results)
#print(target_list)#display result.  If it's working.  Remove
if target not in target_list:
    rprint("[red]TARGET NOT FOUND[/red]")
#import ipdb
#ipdb.set_trace()
