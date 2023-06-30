import json

class Translator:
    def __init__(self):
        self.translations = {
            "en": {},
            "fr": {}
        }

    def load_translations(self):
        try:
            with open("en.json", "r") as f:
                self.translations["en"] = json.load(f)
            with open("fr.json", "r") as f:
                self.translations["fr"] = json.load(f)
        except FileNotFoundError as e:
            print(f"Erreur lors du chargement des fichiers de traduction : {e}")
            sys.exit(1)

    def translate(self, key, lang):
        try:
            return self.translations[lang][key]
        except KeyError:
            return key