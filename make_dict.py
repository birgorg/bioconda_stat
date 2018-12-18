import yaml

def make_dict(path):
    document = open(path, 'r').read()
    return yaml.load(document)

if __name__ == "__main__":
    meta_yaml_dict = make_dict("./meta.yaml")
    print(yaml.dump(meta_yaml_dict))

    print("#"*50)
    print(meta_yaml_dict["package"])
    print("#"*50)
