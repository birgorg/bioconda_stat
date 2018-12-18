import jinja2
from ruamel import yaml

yaml_file = 'meta.yaml'
tmp_file = 'tmp.yaml'

data = yaml.round_trip_load(open(yaml_file))
#data['package']['version'] = '<{ version }>'
with open(tmp_file, 'w') as fp:
    yaml.round_trip_dump(data, fp)

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath='.'),
    trim_blocks=True,
    block_start_string='#%', block_end_string='%#',
    variable_start_string='<{', variable_end_string='}>')
    
print(environment.get_template(tmp_file).render())
