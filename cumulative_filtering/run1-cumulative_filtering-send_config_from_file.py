from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="reader.txt")

northwest_targets = nr.filter(region='north', coast='west') #filtering devices with the region="north" and coast="west" only
results = northwest_targets.run(task=banner_push) #pushing banner_push to specified region/state devices in filtering statement above.
print_result(results)