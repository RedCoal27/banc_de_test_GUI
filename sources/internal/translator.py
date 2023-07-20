import json
import sys
import os

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
            print(f"Erreur lors du chargement des fichiers de traduction : {e}")
            sys.exit(1)
        print("Fichiers de traduction chargés avec succès.")

    def translate(self, key, **kwargs):
        for k, v in kwargs.items():
            kwargs[k] = self.translate(v)
        try:
            translation = self.translations[self.current_language][key]
            return translation.format(**kwargs)
        except KeyError as e:
            # print(f"Erreur lors de la traduction de la clé {key} : clé introuvable.")
            # print(e)
            return key
