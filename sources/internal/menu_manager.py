from PyQt5.QtWidgets import QMenu, QAction, QActionGroup
from PyQt5.QtCore import QTimer

from internal.custom_widget import CustomWidget

from internal.logger import Logger
from window.constant_dialog import ConstantDialog

from window.help_dialog import HelpDialog


class MenuManager:
    """
    La classe MenuManager gère la création et la gestion des menus dans l'interface graphique.

    Attributes:
        parent: Référence à l'objet parent.
        translator: Objet de traduction.
        serial_reader: Lecteur série pour la communication avec les ports COM.

    Methods:
        __init__(self, parent):
            Constructeur de la classe MenuManager.

        create_menus(self):
            Crée les menus dans la barre de menu.

        create_menu(self, menu_name, actions):
            Crée un menu avec les actions spécifiées.

        create_font_size_menu(self):
            Crée le menu de sélection de la taille de la police.

        change_font_size(self, size):
            Change la taille de la police dans les widgets.

        update_com_menu(self):
            Met à jour le menu des ports COM disponibles.

        create_language_menu(self):
            Crée le menu de sélection de la langue.

        change_language(self, lang):
            Change la langue de l'interface graphique.

        open_constant_dialog(self):
            Ouvre la boîte de dialogue pour les constantes.

        open_help_dialog(self):
            Ouvre la boîte de dialogue d'aide.
    """
    def __init__(self, parent):
        """
        Constructeur de la classe MenuManager.

        Args:
            parent: Référence à l'objet parent.
        """
        self.parent = parent
        self.translator = parent.translator
        self.serial_reader = parent.serial_reader

    def create_menus(self):
        """
        Crée les menus dans la barre de menu.
        """
        self.config_menu = QMenu("Config", self.parent)
        self.com_menu = QMenu("COM", self.parent)
        self.help_action = QAction(self.translator.translate("Help"), self.parent)
        self.help_action.triggered.connect(self.open_help_dialog)
        self.com_menu.aboutToShow.connect(self.update_com_menu)
        self.config_menu.addMenu(self.create_language_menu())
        self.config_menu.addMenu(self.create_font_size_menu())
        self.config_menu.addAction("Constante", self.open_constant_dialog)
        self.parent.menuBar().addMenu(self.com_menu)
        self.parent.menuBar().addMenu(self.config_menu)
        self.parent.menuBar().addAction(self.help_action)


    def create_menu(self, menu_name, actions):
        """
        Crée un menu avec les actions spécifiées.

        Args:
            menu_name: Nom du menu.
            actions: Liste des actions du menu.
        """
        menu = QMenu(menu_name, self.parent)
        for action in actions:
            menu.addAction(action)
        return menu

    def create_font_size_menu(self):
        """
        Crée le menu de sélection de la taille de la police.

        Returns:
            Menu de sélection de la taille de la police.
        """
        font_size_menu = QMenu(self.translator.translate("Font size"), self.parent)
        action_group = QActionGroup(self.parent)
        action_group.setExclusive(True)
        for size in [6,7,8,9,10,11,12,13,14]:
            action = QAction(str(size), self.parent)
            action.setCheckable(True)
            if size == self.parent.config["gui"]["font_size"]:  # Check the default font size
                action.setChecked(True)
            action.triggered.connect(lambda checked, s=size: self.change_font_size(s))
            action_group.addAction(action)
            font_size_menu.addAction(action)
        return font_size_menu

    def change_font_size(self, size):
        """
        Change la taille de la police dans les widgets.

        Args:
            size: Taille de la police à définir.
        """
        for item in self.parent.scene.items():
            if isinstance(item, CustomWidget):
                item.set_font_size(size)
        self.parent.config["gui"]["font_size"] = size
        self.parent.config.save_config()
        QTimer.singleShot(0, self.parent.resize_widgets)


    def update_com_menu(self):
        """
        Met à jour le menu des ports COM disponibles.
        """
        self.com_menu.clear()
        action_group = QActionGroup(self.parent)
        action_group.setExclusive(True)
        ports = self.serial_reader.get_available_com_ports()
        if ports:
            for port in ports:
                action = QAction(port, self.parent)
                action.setCheckable(True)
                action.triggered.connect(lambda checked, port=port: self.serial_reader.set_com_port(port))
                action_group.addAction(action)
                self.com_menu.addAction(action)
                if self.serial_reader.ser is not None and self.serial_reader.ser.port == port:
                    action.setChecked(True)
        else:
            self.com_menu.addAction(self.translator.translate("none_available"))

    def create_language_menu(self):
        """
        Crée le menu de sélection de la langue.

        Returns:
            Menu de sélection de la langue.
        """
        language_menu = QMenu(self.translator.translate("language"), self.parent)
        action_group = QActionGroup(self.parent)
        action_group.setExclusive(True)
        for language in self.translator.translations:
            action = QAction(self.translator.translate(language), self.parent)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, lang=language: self.change_language(lang))
            action_group.addAction(action)
            language_menu.addAction(action)
            if language == self.translator.current_language:
                action.setChecked(True)
        return language_menu

    def change_language(self, lang):
        """
        Change la langue de l'interface graphique.

        Args:
            lang: Langue à définir.
        """
        self.translator.current_language = lang
        # self.language_menu.setTitle(self.translator.translate("language"))
        self.config_menu.setTitle(self.translator.translate("Config"))
        self.parent.config["gui"]["lang"] = lang
        self.parent.config.save_config()
        
        

        for item in self.parent.scene.items():
            if isinstance(item, CustomWidget):
                item.change_language()

    def open_constant_dialog(self):
        """
        Ouvre la boîte de dialogue pour les constantes.
        """
        dialog = ConstantDialog(self.parent)
        dialog.exec_()

    def open_help_dialog(self):
        """
        Ouvre la boîte de dialogue d'aide.
        """
        dialog = HelpDialog(self.parent)
        dialog.exec_()