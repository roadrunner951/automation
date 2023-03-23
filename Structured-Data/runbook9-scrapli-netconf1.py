from nornir import InitNornir
from nornir_scrapli.task import netconfig_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def pull_netconf_stuff(task):
    #result = task.run(task=netconfig_get_config, source="running", filters="/native", filter_type="xpath")
    result = task.run(task=netconfig_get_config, source="running", filters="/native/router/ospf/router-id", filter_type="xpath")
results = nr.run(task=pull_netconf_stuff)
print_result(results)