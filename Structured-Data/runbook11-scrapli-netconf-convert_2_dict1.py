from nornir import InitNornir
from nornir_scrapli.task import netconfig_get_config
from nornir_utils.plugins.functions import print_result
import xmltodict

nr = InitNornir(config_file="config.yaml")

def pull_netconf_stuff(task):
    #result = task.run(task=netconfig_get_config, source="running", filters="/native", filter_type="xpath")
    result = task.run(task=netconfig_get_config, source="running", filters="/native/router", filter_type="xpath")
    task.host["facts"] = xmltodict.parse(result.result)
    ospf_rid = task.host["facts"]["rpc-reply"]["data"]["native"]["router"]["ospf"]["router-id"]
    print(f"{task.host} has an OSPF router-id of {ospf_rid}")


results = nr.run(task=pull_netconf_stuff)
#print_result(results)
#import ipdb
#ipdb.set_trace()