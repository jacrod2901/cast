import yaml
from yaml.loader import FullLoader




class YamlReader():
    def __init__(self, configpath):
        self.configpath = configpath

    def get_config_dict(self):
        with open(self.configpath) as file:
            config = yaml.load(file, Loader=FullLoader)
            return config

    
        


    


    


