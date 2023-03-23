from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def get_ip(task):

    response = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = response.scrapli_response.genie_parse_output()#binding to "facts" and running genie parser.
    interfaces = task.host["facts"]
    for intf in interfaces:
        #print(intf)# test if result for loop displays needed data (interfaces).  Remove when done.
        ip_key = interfaces[intf]["ipv4"]
        #print(ip_key)# test if results display the interface IP info. Remove when done.
        for ip in ip_key:
            ip_addr = ip_key[ip]["ip"]
            print(ip_addr)# test 




nr.run(task=get_ip)
#results = nr.run(task=get_ip)
#print_result(results)
import ipdb
ipdb.set_trace()
