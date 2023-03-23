from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="reader.txt")

#north_targets = nr.filter(region='north') #filtering devices with the region key of "north" only
north_targets = nr.filter(state='michigan') # filtering devices with the state ke of "michigan only"
results = north_targets.run(task=banner_push) #pushing banner_push to specified region/state devices in filtering statement above.
print_result(results)