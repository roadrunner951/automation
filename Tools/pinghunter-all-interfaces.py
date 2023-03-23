from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

target_list = []#will append IP addresses of all required IP's on interfaces.
failed_list = []#will append IP's in which cannot be reached (non pingable)

def get_ip(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]
    for intf in interfaces:
        if intf == "Ethernet0/0":#if interface is listed as 'Ethernet0/0'.
            continue#if statement above is true.  Continue runing script.
        ip_add = interfaces[intf]["in_address"]
        if ip_addr != "unassigned":#if ip address is not "unassigned".  Run code below.
            target_list.append(ip_addr)#append to target_list above.


def ping_test(task):
    for ip_address in sorted_list:
        result = task.run(task=send_command, command="ping " + ip_address)#set variable 'result' to use the 'send_command" and ping each 'ip_address' in the 'sorted_list'.
        response = result.result 
        if not "!!!" in response:#if response doesn't get atleast 3 !!! in response variable above.  Run code below.
            failed_list.append(f"{task.host} cannot ping {ip_address}")#append failed_list and print out message.


nr.run(task=get_ip)#execute custom task, 'get_ip".
sorted_list = sorted(target_list)#setting 'sorted_list' variable to sort 'target_list'.
nr.run(task=ping_test)#execute custom task, 'ping_test".