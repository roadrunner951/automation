import ipaddress


subnet = input("Enter the network you wish to test: ")
network = ipaddress.ip_network(subnet)

hosts = network.hosts()
for n in hosts:
    print(n)