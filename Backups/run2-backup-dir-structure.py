#backup script with directory structure

import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file 
from datetime import date
import pathlib

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
#nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
#nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def backup_configurations(task):
    cmds = ["show run", "show ip int brief", "show version"]#send multiple commands using a list.
    for cmd in cmds:
        config_dir = "config-archive"
        date_dir = config_dir + "/" + str(date.today())
        command_dir = date_dir + "/" + cmd
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)
        r = task.run(task=send_command, command=cmd)
        task.run(
            task=write_file,
            content=r.result,
            filename=f"" + str(command_dir + "/" + task.host.name + ".txt",)
        )

results = nr.run(name="Creating Backup Archive", task=backup_configurations)
print_result(results)