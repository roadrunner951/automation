#rollbackup config from flash
from nornir import InitNornir
from nornir_scrapli.tasks import send_command 
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def rollback_config(task):
    task.run(task=send_command, command="configure replace flash:backupconfig force")

results = nr.run(task=rollback_config)
print_result(results)