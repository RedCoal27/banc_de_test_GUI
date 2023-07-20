import json
import sys
import os

from internal.logger import Logger

class Translator:
    def __init__(self):
        self.translations = {
            "en": {},
            "fr": {},
        }
        self.current_language = "en"
        

    def load_translations(self):
        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        parent_path = os.path.dirname(base_path)
        try:
            for language in self.translations:
                lang_path = os.path.join(parent_path, 'lang', f"{language}.json")
                with open(lang_path, "r", encoding="utf-8") as f:
                    self.translations[language] = json.load(f)
        except FileNotFoundError as e:
            Logger.error(f"Error while loading translations: {e}")
            sys.exit(1)
        Logger.info("Translations loaded.")

    def translate(self, key, **kwargs):
        for k, v in kwargs.items():
            kwargs[k] = self.translate(v)
        try:
            translation = self.translations[self.current_language][key]
            return translation.format(**kwargs)
        except KeyError as e:
            return key
