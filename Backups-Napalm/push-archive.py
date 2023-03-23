#Pushing config from text file.
from nornir import InitNornir 
from nornir_scrapli.tasks import send_configs_from_file 
from nornir_utils.plugins.functions import print_result 
from nornir.core.filter import F #filter module


nr = InitNornir(config_file="config.yaml")

def test(task):
    task.run(task=send_configs_from_file, file='eigrpconfig.txt')#point to config file to push.

target = nr.filter(F(hostname="192.168.179.130"))#filtering to only target R1 (192.168.179.130)
results = target.run(task=test)#using target feature to only target R1.
#results = nr.run(task=test)
print_result(results)