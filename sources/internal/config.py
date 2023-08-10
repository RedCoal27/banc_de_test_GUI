import json
import sys
import os

from internal.logger import Logger

class Config:
    """
    Description:
    La classe Config gère la configuration du système. Elle charge et sauvegarde les paramètres à partir d'un fichier JSON.

    Attributes:
        value: Dictionnaire contenant les valeurs de configuration.
        parent: Référence à l'objet parent.
        path: Chemin du fichier de configuration.

    Methods:
        __init__(self, parent):
            Constructeur de la classe Config.

        load_translations(self):
            Charge les paramètres de configuration à partir du fichier JSON.

        save_config(self):
            Sauvegarde les paramètres de configuration dans le fichier JSON.

        __getitem__(self, key):
            Permet d'accéder à une valeur de configuration spécifique.

        get_constant_value(self, key):
            Récupère une valeur constante spécifique de configuration.

        update_text(self):
            Met à jour les valeurs de texte dans les widgets personnalisés.
    """
    def __init__(self, parent):
        """
        Constructeur de la classe Config.

        Args:
            parent: Référence à l'objet parent.
        """
        self.value = {}
        self.parent = parent
        self.path = "config.json"
        self.load_translations()

    def load_translations(self):
        """
        Charge les paramètres de configuration à partir du fichier JSON.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.value = json.load(f)
            Logger.info(f"Configuration file loaded.")

        except FileNotFoundError:
            Logger.error(f"Could not find config file config.json")
            sys.exit(1)

    def save_config(self):
        """
        Sauvegarde les paramètres de configuration dans le fichier JSON.
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.value, f, indent=4) 
        Logger.info(f"Saved config file")
        Logger.debug(f"Config file set to: {self.value}")
        self.update_text()

    def __getitem__(self, key):
        """
        Permet d'accéder à une valeur de configuration spécifique.

        Args:
            key: Clé de la valeur de configuration.

        Returns:
            La valeur de configuration correspondante.
        """
        return self.value[key]

    def get_constant_value(self, key):
        """
        Récupère une valeur constante spécifique de configuration.

        Args:
            key: Clé de la valeur constante.

        Returns:
            La valeur constante correspondante.
        """
        for constant in self.value["constants"]:
            if key in constant["values"]:
                return constant["values"][key]["value"]
        raise KeyError(f"Key {key} not found in constants.")

    def update_text(self):
        """
        Met à jour les valeurs de texte dans les widgets personnalisés.
        """
        self.parent.custom_widgets["MFC1"].update_label("size", value=self.get_constant_value("MFC1"), unit="sccm")
        self.parent.custom_widgets["MFC2"].update_label("size", value=self.get_constant_value("MFC2"), unit="sccm")
