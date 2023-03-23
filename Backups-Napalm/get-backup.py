from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
import pathlib 

nr = InitNornir(config_file="config.yaml")

config_dir = "backup-directory"#change to 

def backup_configurations(task):
    config_result = task.run(task=napalm_get, getters=["config"])
    running_config = config_result.result["config"]["running"]
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    task.run(task=write_file, content=running_config, filename=f"backup-directory/{task.host}.txt")

results = nr.run(task=backup_configurations)
print_result(results)