from importlib import import_module
import argparse
import os

from cast.core.hitapi.hitapi  import MakeApiCall
from cast.core.sqlquerygenerator.query_generator import QueryGenerator
from cast.core.postgres.dbconnect import DbConnect
from cast.core.yamlreader.yamlreader import YamlReader


class BootStrapper:
    DbConnect = None
    QueryGenerator = None
    MakeApiCall = None

    def __init__(self, core_config_path, component_config_path):
        # Reading Component and Core Yaml's
        basepath = self.getbasepath()
        self.coreconfigpath = f'{basepath}/{core_config_path}'
        self.component_config_path = f'{basepath}/{component_config_path}'
        self.core_config = YamlReader(self.coreconfigpath).get_config_dict()
        self.component_config = YamlReader(self.component_config_path).get_config_dict()

        # Initializing all Objects
        self.makeapicall = MakeApiCall()
        self.querygenerator = QueryGenerator()
        self.dbconnect = DbConnect(self.core_config['db-config'])

        
        # Making Component Call
        
        component_root =  self.core_config['component-root']
        component_name = self.component_config['component-name']
        component_path = component_root + '.' + component_name
        moduleobject = self.importComponentModule(component_path)
        contextvar = self.buildContextVar()
        moduleobject.driver(contextvar)


    def importComponentModule(self, modulepath):
        moduleobject = import_module(modulepath)
        return moduleobject        


    def buildContextVar(self):
        contextvar = {}
        contextvar['querygenerator'] = self.querygenerator
        contextvar['makeapicall'] = self.makeapicall
        contextvar['dbconnect'] = self.dbconnect
        contextvar['componentconfig'] = self.component_config
        contextvar['coreconfig'] = self.core_config
        return contextvar

    def getbasepath(self):
        basepath = os.getcwd()
        return basepath


def main(args):
    core_config_path = args.coreconfig
    component_config_path = args.componentconfig
    bs = BootStrapper(core_config_path,component_config_path )
    print('<<<<< Complete >>>>>>>')





if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--coreconfig", help='Please enter core config path')
    parser.add_argument("--componentconfig", help='please Component config path')
    args = parser.parse_args()
    main(args)