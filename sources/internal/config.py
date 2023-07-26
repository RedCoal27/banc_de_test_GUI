import json
import sys
import os

from internal.logger import Logger

class Config:
    def __init__(self):
        self.value = {}
        self.path = "config.json"
        self.load_translations()

    def load_translations(self):
        #print file at root
        print(os.listdir())
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.value = json.load(f)
            Logger.info(f"Configuration file loaded.")

        except FileNotFoundError:
            Logger.error(f"Could not find config file config.json")
            sys.exit(1)
                    
    def edit_config(self, key, value):
        self.value[key] = value
        print(self.value[key])
        #save json
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.value, f, indent=4) 
        Logger.info(f"Edited config file: {key} = {value}")

    def save_config(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.value, f, indent=4) 
        Logger.info(f"Saved config file: {self.value}")

    def __getitem__(self, key):
        return self.value[key]
    


