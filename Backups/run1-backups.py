#backup script

import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file 

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def backup_configurations(task):
    cmds = ["show run", "show version"]#send multiple commands using a list.
    for cmd in cmds:
        r = task.run(task=send_command, command=cmd)
        task.run(task=write_file, content=r.result, filename=f"{cmd}-{task.host}.txt")#using f string to name each file per the command used and device name to save locally.

results = nr.run(name="Creating Backup Archive", task=backup_configurations)
print_result(results)