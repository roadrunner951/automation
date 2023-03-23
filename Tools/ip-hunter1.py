import threading#allows for thread control
import os#to clear screen
from collections import Counter
from rich import print as rprint
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F#filter module as F

nr = InitNornir(config_file="config.yaml")

ip_list = []#All IP's from script will be appended in here as the loop interates.  Globally accessible.

CLEAR = "clear"#set CLEAR variable
os.system(CLEAR)#CLEAR variable runs and clears screen
LOCK = threading.Lock()#lock variable to initialize threading
filtered = False#filtered set to off initially

answer = input("Would you like to a apply a location filter to this script? <y/n> ")
if answer == "y":
    filtered = True#filtered now enabled
    location = input("Select a location to target: ")
    filtered_type = input("Do you want to include or exclude this location? <include/exclude> ")
    if filtered_type == "exclude": #will not include location
        filtered_hosts = nr.filter(~F(location=location))#filter will now exclude the location key
    else:
        filtered_hosts = nr.filter(F(location=location))#filter will now include the locatin key

def get_ip(task):

    response = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = response.scrapli_response.genie_parse_output()#binding to "facts" and running genie parser.
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                #print(ip_addr)#test if IP dipslay.  Remove when done.
                ip_list.append(ip_addr)
        except KeyError:
            pass

def locate_ip(task):
    response = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = response.scrapli_response.genie_parse_output()#binding to "facts" and running genie parser.
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                if ip_addr in targets:
                    version_result = task.run(task=send_command, command="show version")
                    task.host["verfacts"] = version_result.scrapli_response.textfsm_parse_output()#binding to "verfacts" and running textfsm parser.
                    serial = task.host["verfacts"][0]["serial"][0]
                    LOCK.acquire()#locks terminal as program is writing to it.
                    rprint(f"[yellow]{task.host} {intf} - {ip_addr}[/yellow]")
                    rprint("[cyan]RETRIEVING DEVICE DATA...[/cyan]")
                    print(f"SERIAL NUMBER: {serial}")
                    print(f"MGMT IP: {task.host.hostname}")
                    data = task.host.data
                    for k, v in data.items():
                        if "facts" not in k:
                            print(f"{k}: {v}")
                    print("\n")#new line
                    LOCK.release()#after finishing printing to terminal.  Lock will be released.

        except KeyError:
            pass


#nr.run(task=get_ip)
#results = nr.run(task=get_ip)
if filtered:
    filtered_hosts.run(task=get_ip)
    targets = [k for k, v in Counter(ip_list).items() if v > 1]
    if targets:
        rprint("[red]ALERT: DUPLICATES DETECTED![/red]")
        rprint(targets)
        rprint("\n[cyan]Locating addresses in topology.../[cyan]\n")
        filtered_hosts.run(task=locate_ip)
    else:
        rprint("[green]SCAN COMPLETED - NO DUPLICATES DETECTED[/green]")


else:
    nr.run(task=get_ip)
    targets = [k for k, v in Counter(ip_list).items() if v > 1]
    if targets:
        rprint("[red]ALERT: DUPLICATES DETECTED![/red]")
        rprint(targets)
        rprint("\n[cyan]Locating addresses in topology...[/cyan]\n")

        nr.run(task=locate_ip)
    else:
        print("[green]SCAN COMPLETED - NO DUPLICATES DETECTED[/green]")
#print(targets)
#print_result(results)
#print(ip_list)#test empty list (ip_list) if IP's append.  Comment/Remove when done.
#import ipdb
#ipdb.set_trace()
