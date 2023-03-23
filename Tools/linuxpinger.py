import ipaddress
from subprocess import Popen, DEVNULL
from rich import print as rprint
from rich.console import Console 
from rich.table import Table
import itertools
import time


ping = {}
active_list = []
inactive_list = []

localtime = time.asctime(time.localtime(time.time()))

rprint("[green]Welcome to LinuxPinger![/green]")
rprint("[cyan]Please enter the network you wish to test...[/cyan]")
rprint("Example: <192.168.10.0/24>")
subnet = input("Enter network: ")
network = ipaddress.ip_network(subnet)

hosts = network.hosts()
for n in hosts:
    IP = str(n)
    ping[IP] = Popen(['ping', '-c', '4', '-i', '0.2', IP], stdout=DEVNULL)

while ping:
    for IP, process in ping.items():
        if process.poll() is not None:
            del ping[IP]
            if process.returncode == 0:
                active_list.append(IP)
            elif process.returncode == 1:
                inactive_list.append(IP)
            else:
                print(f"{IP} ERROR")
            break



table = Table(title="PING REPORT \n" + localtime)
table.add_column("Active Hosts", justify="center", style="green")
table.add_column("Inactive Hosts", justify="center", style="red")
for (a, i) in itertools.zip_longest(active_list, inactive_list):
    table.add_row(a, i)
console = Console()
console.print(table)