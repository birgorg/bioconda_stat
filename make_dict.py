from pathlib import Path
import yaml
import argparse
import os
import toyamel

numExc = 0

def walklevel(some_dir, level=0):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def make_dict(path):
    try:
        document = open(path, 'r').read()
        document = toyamel.dynamic_jinja_to_static_yaml(path)
        return yaml.load(document)
    except yaml.YAMLError as exc:
        print(exc)
        global numExc
        numExc += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs through a bioconda recipes and operates on .yamel files")
    parser.add_argument('bioconda_path', help='path to bioconda/recipes')
    args = parser.parse_args()

    numGithub = 0 
    numDir = 0 
    gitUrls = []
    dir_path = args.bioconda_path
    for subdir, dirs, files in os.walk(dir_path):
        for i in dirs:
            print('Dirs: '+i)
            path = "{}{}/meta.yaml".format(dir_path, i)
            if not Path(path).is_file():
                continue
            print(path)
            meta_yaml_dict = make_dict(path)
            if meta_yaml_dict != None:
                if 'source' in meta_yaml_dict:
                    numDir += 1
                    url = ""
                    if isinstance(meta_yaml_dict['source'], list) and 'url' in meta_yaml_dict['source'][0]:
                        url = meta_yaml_dict['source'][0]['url']
                    elif 'url' in meta_yaml_dict['source']:
                        url = meta_yaml_dict['source']['url']
                    print(url)
                    if 'github' in url:
                        gitUrls.append(url)
                        numGithub += 1

            print('total: '+str(numGithub)+' of '+str(numDir))
    print('total: '+str(numGithub)+' of '+str(numDir))
    print('Number of Jinja exceptions: '+str(numExc))
    with open('githubUrls.txt', 'w') as f:
        for u in gitUrls:
            f.write(u+'\n')
