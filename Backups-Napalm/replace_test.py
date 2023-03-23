#Replaced device current config with backup 'get-backup.py' if there's any differences.  
#Note:  Take note of banner config will cause readtimeout error messages.  Apply fix stated in videos/notes under section 'Napalm Replace'.

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def replace_stuff(task):
    task.run(task=napalm_configure, filename=f"backup-directory/{task.host}.txt", replace=True)
    read_timeout=90


results = nr.run(task=replace_stuff)
print_result(results)
