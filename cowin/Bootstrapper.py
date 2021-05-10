from importlib import import_module
import argparse

from cast.core.hitapi.hitapi  import MakeApiCall
from cast.core.sqlquerygenerator.query_generator import QueryGenerator
from cast.core.postgres.dbconnect import DbConnect
from cast.core.yamlreader.yamlreader import YamlReader


class BootStrapper:
    DbConnect = None
    QueryGenerator = None
    MakeApiCall = None

    def __init__(self, core_config_path, component_config_path):
        # component_root = YamlReader.get_config_dict(core_config_path)['component-root']
        # component_name = YamlReader.get_config_dict(component_config_path)['component-name']
        component_root = 'cast.components'
        component_name = 'test.test5'
        component_path = component_root + '.' + component_name
        moduleobject = self.importComponentModule(component_path)
        contextvar = self.buildContextVar()
        contextvar = {'A':5}
        moduleobject.driver(contextvar)


    def importComponentModule(self, modulepath):
        moduleobject = import_module(modulepath)
        return moduleobject        


    def buildContextVar(self):
        contextvar = {}
        return contextvar




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