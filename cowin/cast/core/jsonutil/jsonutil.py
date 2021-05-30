import json
import datetime

class JsonUtil:
    def __init__(self, json_config):
        self.__jsonfilepath = json_config['json-file-path']

    
    def __readJson(self):
        f = open(self.__jsonfilepath)
        __json_content = json.load(f)
        f.close()
        return __json_content

    def __writeJson(self, content):
        f = open(self.__jsonfilepath, 'w')
        json.dump(content, f)
        f.close()

    def updateDocumentTS(self):
        json_content = self.__readJson()
        json_content['last-apidata-timestamp'] = str(datetime.datetime.now())
        self.__writeJson(json_content)

    def getJsonData(self):
        return self.__readJson()














