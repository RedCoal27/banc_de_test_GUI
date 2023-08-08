import json
import sys
import os

import time

from internal.logger import Logger

class Translator:
    def __init__(self,config):
        self.translations = {
            "en": {},
            "fr": {},
            "gilles":{},
        }
        self.current_language = config["gui"]["lang"]
        

    def load_translations(self):
        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        parent_path = os.path.dirname(base_path)
        #print list of files in the directory
        try:
            for language in self.translations:
                lang_path = os.path.join(parent_path, 'lang', f"{language}.json")
                with open(lang_path, "r", encoding="utf-8") as f:
                    self.translations[language] = json.load(f)
        except FileNotFoundError as e:
            Logger.error(f"Error while loading translations: {e}")
            time.sleep(1000)
            sys.exit(1)
        Logger.info("Translations loaded.")
        
    def translate(self, key, **kwargs):
        if not isinstance(key,str):
            key = str(key)
        for k, v in kwargs.items():
            kwargs[k] = self.translate(v)
        try:
            # Try to get the translation in the current language
            translation = self.translations[self.current_language][key]
        except KeyError:
            # If not found, fallback to English
            translation = self.translations["en"].get(key, key)
        try:
            translation = translation.format(**kwargs)
            return translation
        except:
            return key
