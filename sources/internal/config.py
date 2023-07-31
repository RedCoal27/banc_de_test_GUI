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
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.value = json.load(f)
            Logger.info(f"Configuration file loaded.")

        except FileNotFoundError:
            Logger.error(f"Could not find config file config.json")
            sys.exit(1)

    def save_config(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.value, f, indent=4) 
        Logger.info(f"Saved config file")
        Logger.debug(f"Config file set to :{self.value}")

    def __getitem__(self, key):
        return self.value[key]

    def get_constant_value(self, key):
        for constant in self.value["constants"]:
            if key in constant["values"]:
                return constant["values"][key]["value"]
        raise KeyError(f"Key {key} not found in constants.")
