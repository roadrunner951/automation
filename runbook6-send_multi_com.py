from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

#sending multiple commands - 1
command_list = ["show ip interface brief", "show version", "show run"]

def show_command_test(task):
    #sending multiple commands - 2
    for cmd in command_list:
        task.run(task=send_command, command=cmd)

results = nr.run(task=show_command_test)
print_result(results)
