from ipaddress import ip_network, ip_address#imports ipaddress module.
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F#filter module
from rich import print as print
import json#import json module


nr = InitNornir(config_file="config.yaml")

target = input("Enter the targert IP: ")#ask user to input target ip and sets value inside 'target' variable.
ipaddr = ip_address(target)#set ipaddr variable using the ip_address module referrencing 'target' variable above.
my_list = []

def get_cisco(task):#defining get_routes function with passing the 'task' arugment

    response = task.run(task=send_command, command="show ip route")#setting response variable to use the 'send_command' feature while using the command 'show ip route'.
    task.host["facts"] = response.scrapli_response.genie_parse_output()#bind devices to "facts" key and run genie parser to locate appropriate keys/values to parse.  Run ipdb after this to locate values needed.
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]#created per the genie parser output and ipdb debugger to locate required keys/values to parse.
    for prefix in prefixes:#iterate all routes from the prefixes variable above
        #print(prefix)#check if above parse is working.  Remove/Comment out when complete.  Only for testing.
        net = ip_network(prefix)#setting the 'net' variable to use the ip_network feature using the arguement 'prefix'. 'Prefix' being the variable used in the for loop to iterate through the current ip routes.
        if ipaddr in net:#if conditional statement to check if ip address target used is present in any of the availble networks.
            #print(f"{ipaddr} is present on device {task.host} (network: {net})")#if statement above is true.  Print this message.  This is for testing only.  Remove/comment when done.
            source_proto = prefixes[prefix]["source_protocol"]#setting the source_proto
                if source_proto = "connected":#'if' source_proto(source_protcol key) says 'connected'.  Try to run the code below.
                    try:#will attempt the code below
                        outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]#set outgoing_intf variable parsing out 'outgoing_interface' values.
                        for intf in outgoing_intf:#using 'for' loop to iterate through the 'outgoing_interface'(outgoing_intf)
                            exit_intf = intf#setting variable exist_intf from the output above.
                            my_list.append(f"{task.host} is connected to {target} via interface {exist_intf}")#will append to global empty list named 'my_list'
                            print(f"{task.host} is connected to {target} via interface {exit_intf}")#printing this message per code block above.
                    except KeyError:#if KeyError is raised it will it not raise any error messages of any kind
                        pass#code will continue to run without any error codes.

                else:#if code try block is not ran, code block below will run as an alternative.
                    try:
                        net_hop_list = prefixes[prefix]["next_hop"]["next_hop_list"]
                        route_preference = prefixes[prefix]["route_preference"]
                        for key in next_hop_list:
                            next_hop = next_hop_list[key]["next_hop"]
                            if route_preference == 20:
                                source_proto = "eBGP"
                            elif route_preference == 200:
                                source_proto = "iBGP"
                            my_list.append(f"{task.host} can reach {target} via next hop: {next_hop} ({source_proto})")#will append to global empty list named 'my_list'
                            print(f"{task.host} can reach{target} via next hop {next_hop} ({source_proto})")
                    except KeyError:
                        pass

def get_arista(task):
    result = task.run(task=send_command, command="show ip route | json")#set results variable to use 'send_command' and send command "show ip route | json" to arista devices only.
    task.host["facts"] = json.loads(result.result)#bind arista devices to the 'facts' key to display results from the code above.  Add 'json.loads(result.result) to format output to a dictionary view via json module.
    #testvariable = task.host["facts"]#set testvariable to display output from 'facts' key.
    #print(type(testvariable))#print output from testvariable and dislay type of data presented.  Only for testing.  Remove/comment out when done.
    prefixes = task.host["facts"]["vrfs"]["default"]["routes"]#path obtained via ipdb debugger.  Here we set the variable 'prefixes' after learning the path using ipdb to routes key.
    for prefix in prefixes:#for loop to iterate through the routes key
    net = ip_network(prefix)#net variable set to use ip_network feature and pass 'prefix' variable from above.
    if ipaddr in net:#if ipaddr(ip inputted by user in 'net', routes from output above)
        route_type = prefixes[prefix]["routeType"]#set route_type variable for output from 'routeType' key.
        vias = prefixes[prefix]["vias"]#set vias variable for 'vias' output.
        for via in vias:#for loop to iterate through each device 'vias' output result per device
            exit_intf = via["interface"]#set 'exit_intf" variable via 'inteface' key.
            if route_type == "connected":#if 'routeType' key value is set to 'connected'.  Run code block below.
                my_list.append(f"{task.host} is connected to {target} via interface {exit_intf}")#
            else:#if 'routeType' output result is not set to 'connected' then run code below instead.
                next_hop = via["nexthopAddr"]#set 'next_hop' variable via 'nexthopAddr' key on device.
                my_list.append(f"{task.host} can reach {target} via next hop: {next_hop} ({route_type})")

cisco = nr.filter(F(platform="ios"))#set 'cisco' variable to run filter on ios(cisco) devices.
cisco.run(task=get_cisco)#initialize variable above and run code block 'get_cisco'.

arista = nr.filter(F(platform="eos"))#set 'arista' variable to run filter on ios(cisco) devices.
arista.run(task=get_arista)#initialize variable above and run code block 'get_arista'.
#nr.run(task=get_cisco)
if my_list:#if my_list has values in it(equals to True), run code below.
    sorted_list = sorted(my_list)
    rprint(sorted_list)

else:#if my_list has no values(equals to False) run code below instead.
    rprint(f"{target} is not reachable")
#sorted_list = sorted(my_list)#sorts my_list output
#rprint(sorted_list)#use rprint with sorted list output
#print(my_list)
import ipdb
ipdb.set_trace()