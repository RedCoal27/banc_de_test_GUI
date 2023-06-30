import json
import sys

class Translator:
    def __init__(self):
        self.translations = {
            "en": {},
            "fr": {},
        }
        self.current_language = "en"

    def load_translations(self):
        try:
            for language in self.translations:
                with open(f"lang/{language}.json", "r", encoding="utf-8") as f:
                    self.translations[language] = json.load(f)
        except FileNotFoundError as e:
            print(f"Erreur lors du chargement des fichiers de traduction : {e}")
            sys.exit(1)

    def translate(self, key, **kwargs):
        try:
            translation = self.translations[self.current_language][key]
            return translation.format(**kwargs)
        except KeyError:
            return key
