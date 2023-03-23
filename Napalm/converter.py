import yaml
from pprint import pprint

#output from 'get_facts.py'
target_dict = { 'get_facts': { 'fqdn': 'R1.cisco.com',
                 'hostname': 'R1',
                 'interface_list': [ 'GigabitEthernet0/0',
                                     'GigabitEthernet0/1',
                                     'GigabitEthernet0/2',
                                     'GigabitEthernet0/3',
                                     'Loopback0'],
                 'model': 'IOSv',
                 'os_version': 'IOSv Software (VIOS-ADVENTERPRISEK9-M), '
                               'Version 15.9(3)M3, RELEASE SOFTWARE (fc1)',
                 'serial_number': '9AGYLEFO9KRQBQ51JLRPA',
                 'uptime': 52320.0,
                 'vendor': 'Cisco'}}


filename = "validate-R1.yaml"#will generate file using data in target_dict.
with open(filename, "w") as f:
    output = yaml.dump(target_dict, f, default_flow_style=False)