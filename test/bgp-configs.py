from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs 
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml


nr = InitNornir(config_file="config.yaml")

def load_vars(task):
    loader = task.run(task=load_yaml, file=f"host_vars1/{task.host}.yaml")
    task.host["facts"] = loader.result 
    push_bgp(task)


def push_bgp(task):
    template = task.run(task=template_file, template="bgp.j2", path="templates")
    task.host["bgp_config"] = template.result
    rendered = task.host["bgp_config"]
    #print(rendered)#print check only.  
    configuration = rendered.splitlines()#will create for each device to feed to scrapli send_configs function.
    task.run(task=send_configs, configs=configuration)

results = nr.run(task=load_vars)
print_result(results)