import sys
from PyQt5.QtWidgets import QMenu, QAction, QActionGroup
from PyQt5.QtCore import QTimer
from serial.tools.list_ports import comports
from custom_widget import CustomWidget

from logger import logger


class MenuManager:
    def __init__(self, parent):
        self.parent = parent
        self.translator = parent.translator
        self.serial_reader = parent.serial_reader

    def create_menus(self):
        self.config_menu = QMenu("Config", self.parent)
        self.com_menu = QMenu("COM", self.parent)
        self.com_menu.aboutToShow.connect(self.update_com_menu)
        self.config_menu.addMenu(self.create_language_menu())
        self.config_menu.addMenu(self.create_font_size_menu())
        self.parent.menuBar().addMenu(self.com_menu)
        self.parent.menuBar().addMenu(self.config_menu)

    def create_menu(self, menu_name, actions):
        menu = QMenu(menu_name, self.parent)
        for action in actions:
            menu.addAction(action)
        return menu

    def create_font_size_menu(self):
        font_size_menu = QMenu(self.translator.translate("Font size"), self.parent)
        action_group = QActionGroup(self.parent)
        action_group.setExclusive(True)
        for size in [6,7,8,9,10,11,12,13,14]:
            action = QAction(str(size), self.parent)
            action.setCheckable(True)
            if size == 8:  # Check the default font size
                action.setChecked(True)
            action.triggered.connect(lambda checked, s=size: self.change_font_size(s))
            action_group.addAction(action)
            font_size_menu.addAction(action)
        return font_size_menu

    def change_font_size(self, size):
        for item in self.parent.scene.items():
            if isinstance(item, CustomWidget):
                item.police_size = size
        QTimer.singleShot(0, self.parent.resize_widgets)

    def update_com_menu(self):
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
        self.translator.current_language = lang
        # self.language_menu.setTitle(self.translator.translate("language"))
        self.config_menu.setTitle(self.translator.translate("Config"))
        
        for key, button_tuple in self.parent.buttons.items():
            button = button_tuple[0]
            button.setText(self.translator.translate(key))

        for item in self.parent.scene.items():
            if isinstance(item, CustomWidget):
                item.change_language()
