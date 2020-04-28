import yaml
import os
import io

class Config:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        yamlPath = os.path.join(path, "config.yml")
        self.raw = io.open(yamlPath, 'r', encoding="utf-8").read()
        self.cfg = yaml.load(self.raw)
        pass

    def getConfig(self, key = None):
        if (key):
            return self.cfg[key]
        else:
            return self.cfg