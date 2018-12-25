import jinja2
from ruamel import yaml
import re

"""helper function: converts {% to #% and {{ to <{"""
def convert_line(line, jinja_configs):  
    # 'greedy' check that seems to be enough 
    # (there might still be some other elements 
    # in the line that has {{ ... }} or {% ... %} around it)  
    if any(conf in line for conf in jinja_configs):
        line = line.replace("{{", "<{")
        line = line.replace("}}", "}>")
        line = line.replace("{%", "#%")
        line = line.replace("%}", "%#")

    # remove conda's own 'compiler' syntax (that the yaml parser wont accept)
    if "{{" in line:
        result = re.search('{{ compiler(.*)}}', line)
        line = ""

    return line

"""converts the jinja syntax in a yaml file,
    into a syntax that can be used by ruamel"""
def convert_jinja_syntax(file_to_convert):
    new_file = ""
    jinja_configs = set()

    with open(file_to_convert, 'r') as fp:
        for line in fp:
            if "{%" in line:
                result = re.search('{% set (.*)=', line)
                jinja_configs.add(result.group(1).strip())

            new_file += convert_line(line, jinja_configs)
    
    with open(file_to_convert, 'w') as fp:
        fp.write(new_file)
    

def dynamic_jinja_to_static_yaml(filename):
    tmp_file = 'tmp.yaml'

    convert_jinja_syntax(filename)
    
    data = yaml.round_trip_load(open(filename))
    with open(tmp_file, 'w') as fp:
        yaml.round_trip_dump(data, fp)

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='.'),
        trim_blocks=True,
        block_start_string='#%', block_end_string='%#',
        variable_start_string='<{', variable_end_string='}>')

    try:
        return environment.get_template(tmp_file).render()
    except:
        print("ERROR in dynamic_jinja_to_static_yaml")
        return ""
