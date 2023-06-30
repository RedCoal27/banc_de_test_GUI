import json
import sys

class Translator:
    def __init__(self):
        self.translations = {
            "en": {},
            "fr": {}
        }
        self.current_language = "en"

    def load_translations(self):
        try:
            with open("lang/en.json", "r", encoding="utf-8") as f:
                self.translations["en"] = json.load(f)
            with open("lang/fr.json", "r", encoding="utf-8") as f:
                self.translations["fr"] = json.load(f)
        except FileNotFoundError as e:
            print(f"Erreur lors du chargement des fichiers de traduction : {e}")
            sys.exit(1)

    def translate(self, key, **kwargs):
        try:
            translation = self.translations[self.current_language][key]
            return translation.format(**kwargs)
        except KeyError:
            return key
