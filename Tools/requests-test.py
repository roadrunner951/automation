import requests
import ipaddress
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from collections import defaultdict
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")#initialize nornir
requests.packages.urllib3.disable_warnings()#disables warning messages.  Only for lab environments.

headers = { 'Accept': 'application/yang-data+json'}#headers variable to use application, yang-data with json.

config_dict = defaultdict(dict)#using 'defaultdict' for 'ospf-config' data.
facts_dict = defaultdict(dict)#using 'defaultdict' for 'ospf-facts' data.

def get_ospf(task):#renamed from 'testconf' to 'get_ospf'.
    ospf_url = f"https://{task.host.hostname}:443/restconf/data/ospf-oper-data"#sends https requests for ospf data via restconf protocol.
    ospf_send = requests.get(url=ospf_url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)#authenticates in url above to obtain structured data
    #print(response.text)#testing purposes only.  Remove/comment out when done.
    #return Result(host=task.host, result=response.text)#testing purposes only.  Remove/comment out when done.

    inter_url = f"https://{task.host.hostname}:443/restconf/data/native/interface"#sends https request for ospf interface data via restconf protocol.
    inter_send = requests.get(url=inter_url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)#authenicates in url above to obtain structured data.

    task.host["ospf-facts"] = ospf_send.json()#binds to key 'ospf-facts' to obtain ospf data via json format.
    task.host["ospf-config"] = inter_send.json()#binds  to key 'ospf-config' to obtain ospf interface data via json format.

    config_interfaces = task.host["ospf-config"]["Cisco-IOS-XE-native:interface"]#set 'config-interfaces' variable for each interfaces on device.
    for inter_type in config_interfaces:#loops through all interfaces on device
        interfaces = config_interfaces[inter_type]#interface type data
        for intf in interfaces:#for loop to iterate through interfaces
            #print(intf)#for testing only
            try:
                name = intf["name"]#name avariable for interface name data
                intlink = inter_type + str(name)
                ip = intf["ip"]["address"]["primary"]["address"]#ip variable for IP address of interface data.
                mask = intf["ip"]["address"]["primary"]["mask"]#mask variable for subnet mask data.
                #print(f"{task.host} interface{name} - {ip}/{mask}")#will display output using f string and variables.  For testing only.
                config_dict [f"{task.host}"][intlink] = [ip, mask]#prints out using variables via f string.

            except KeyError:
                pass

    instances = task.host["ospf-facts"]["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"]
    for instance in instances:
        areas = instance["ospf-area"]
        for area in areas:
            try:
                area_id = area["area-id"]
                #print(f"The area ID is {area_id}")#testing only.
                ospf_interfaces = area["ospf-interface"]
                for ospf_interface in ospf_interfaces:#looping through 'interfaces' key to extract data.
                    name = ospf_interface["name"]#name variable that extracts name value in 'interfaces' loop.
                    dead = ospf_interface["dead-interval"]#dead variable that extracts 'dead-interval' in 'interfaces' loop.
                    hello = ospf_interface["hello-interval"]#hello variable that extracts 'hello-interval' in 'interfaces' loop.
                    #print(f"interface {name} has a hello of {hello} and a dead of {dead}")#testing only
                    facts_dict [f"{task.host}"][name] = [dead, hello, area_id]#prints out using variables via f string.


            except KeyError:
                pass

def get_cdp(task):#renamed from 'testconf' to 'get_ospf'.
    cdp_url = f"https://{task.host.hostname}:443/restconf/data/cdp-neighbor-details"#sends https requests via restconf protocol to get cdp neighbor data to parse.
    response = requests.get(url=cdp_url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)#authenticates in url above to obtain structured data
    task.host["cdp-facts"] = response.json()
    cdp_neighbors = task.host["cdp-facts"]["Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"]["cdp-neighbor-detail"]
    for neighbor in cdp_neighbors:
        dev_name = neighbor["device-name"]
        local_intf = neighbor["local-intf-name"]
        port_id = neighbor["port-id"]
        #rprint(f"{task.host} interface {local_intf} is connected to {dev_name} on its {port_id} interface")#Test only.  Remove/comment out when done.
        if local_intf.startswith("Gi"):
            try:
                local_ip = config_dict[f"{task.host}"][local_intf][0]
                rprint(f"{task.host} interface {local_intf} has an IP address of {local_ip}")#Test Only. 
                local_mask = config_dict[f"{task.host}"][local_intf][1]
                rprint(f"{task.host} {local_intf} = {local_ip}/{local_mask}")#test
                local_net = ipaddress.ip_network(local_ip + "/" + local_mask, strict=False)
                rprint(f"{task.host} {local_intf} = {local_net}")#test
                remote_ip = config_dict[dev_name][port_id][0]
                remote_mask = config_dict[dev_name][port_id][1]
                remote_net = ipaddress.ip_network(remote_ip + "/" + remote_mask, strict=False)
                rprint(f"{task.host} {local_intf} {local_net} - connected to {dev_name} {port_id} {remote_net}")
            except KeyError:
                pass        
            
        


ospf_results = nr.run(task=get_ospf)
cdp_results = nr.run(task=get_cdp)
#print_result(cdp_results)
#rprint(config_dict)
#print("\n\n")
#rprint(facts_dict)
#import ipdb 
#ipdb.set_trace()