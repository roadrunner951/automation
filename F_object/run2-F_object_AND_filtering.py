'''
Install apps below

python3 -m pip install nornir
python3 -m pip install nornir-scrapli
python3 -m pip install nornir_utils
'''
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F # F object filtering

nr = InitNornir(config_file="config.yaml")

#using environment variables for credentials
nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="reader.txt")

legend_on_the_court = nr.filter(F(legend=True) & F(location='court')) #filtering devices with the legends=True including using the AND logic to filter similar as cumulative.
results = legend_on_the_court.run(task=banner_push) #pushing banner_push to specified devices that is mapped to the legends and courts keys in groups.yaml.  Also mapped on hosts.yaml file.
print_result(results)