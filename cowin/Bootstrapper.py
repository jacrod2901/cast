from importlib import import_module
import argparse
import os, sys

from cast.core.hitapi.hitapi  import MakeApiCall
from cast.core.sqlquerygenerator.query_generator import QueryGenerator
from cast.core.postgres.dbconnect import DbConnect
from cast.core.yamlreader.yamlreader import YamlReader
from cast.core.emailutil.emailutil import EmailUtil

parentPath = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir
)


if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

class BootStrapper:
    DbConnect = None
    QueryGenerator = None
    MakeApiCall = None

    def __init__(self, core_config_path, component_config_path):
        # Reading Component and Core Yaml's
        # self.basepath = self.getbasepath()
        self.coreconfigpath = core_config_path
        self.component_config_path = component_config_path
        self.core_config = YamlReader(self.coreconfigpath).get_config_dict()
        self.component_config = YamlReader(self.component_config_path).get_config_dict()

        # Initializing all Objects
        self.makeapicall = MakeApiCall()
        self.querygenerator = QueryGenerator()
        self.dbconnect = DbConnect(self.core_config['db-config'])
        self.emailutil = EmailUtil(self.core_config['email-config'])

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
        contextvar['emailutil'] = self.emailutil
        contextvar['componentconfig'] = self.component_config
        contextvar['coreconfig'] = self.core_config
        # contextvar['basepath'] = self.basepath
        return contextvar

    def getbasepath(self):
        basepath = os.getcwd()
        return basepath


def main(args):
    core_config_path = args.coreconfig
    component_config_path = args.componentconfig
    bs = BootStrapper(core_config_path,component_config_path )
    print('<<<<< Bootstrapper Complete >>>>>>>')





if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--coreconfig", help='Please enter core config path')
    parser.add_argument("--componentconfig", help='please Component config path')
    args = parser.parse_args()
    main(args)