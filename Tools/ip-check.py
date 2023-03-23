from ipaddress import ip_network, ip_address
target = input("Enter the target IP address: ")
ipaddr = ip_address(target)#ipaddr variable referrencing above input 'target' variable.  Depending the IP used.

#print(ipaddr)
ip_list = ["10.0.0.0/30", "10.0.0.4/30"]

for prefix in ip_list:#using for loop.  Setting 'prefix' variable to iterate through the ip_list (each IP in ip_list).
    net = ip_network(prefix)#using the ip_network function and passing argument 'prefix' to parse out network info.
    if ipaddr in net:
        print(f"{ipaddr} in is the {net} network")