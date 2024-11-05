import yaml

def parse_yaml(yaml_file):
    with open(yaml_file, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.FullLoader)
