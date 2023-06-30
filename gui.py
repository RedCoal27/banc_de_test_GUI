import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QAction, QMessageBox, QActionGroup
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette
from PyQt5.QtCore import Qt, QTimer
import serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException
import json

from translator import Translator
from serial_reader import SerialReader



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_reader = SerialReader()

        self.buttons = {}

        self.translator = Translator()
        self.translator.load_translations()
        self.current_language = "en"

        self.init_ui()

    def init_ui(self):
        self.create_timer()
        self.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Interface PyQt5")
        self.setMinimumSize(600, 400)

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_menus(self):
        self.com_menu = QMenu("COM", self)
        self.com_menu.aboutToShow.connect(self.update_com_menu)
        self.menuBar().addMenu(self.com_menu)

        self.menuBar().addMenu(self.create_language_menu())


    def create_menu(self, menu_name, actions):
        menu = QMenu(menu_name, self)
        for action in actions:
            menu.addAction(action)
        return menu
    
    def update_com_menu(self):
        self.com_menu.clear()
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        ports = self.serial_reader.get_available_com_ports()
        if ports:
            for port in ports:
                action = QAction(port, self)
                action.setCheckable(True)
                action.triggered.connect(lambda checked, port=port: self.serial_reader.set_com_port(port))
                action_group.addAction(action)
                self.com_menu.addAction(action)
                if self.serial_reader.ser is not None and self.serial_reader.ser.port == port:
                    action.setChecked(True)
        else:
            self.com_menu.addAction("Aucun disponible")

    def create_language_menu(self):
        language_menu = QMenu(self.translator.translate("language", self.current_language), self)
        for language in ["en", "fr"]:
            action = QAction(self.translator.translate(language, self.current_language), self)
            action.triggered.connect(lambda checked, lang=language: self.change_language(lang))
            language_menu.addAction(action)
        return language_menu
    
    def change_language(self, lang):
        self.current_language = lang
        for key, button_tuple in self.buttons.items():
            button = button_tuple[0]
            button.setText(self.translator.translate(key, self.current_language))



    def create_background_and_buttons(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setCentralWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem(QPixmap("background.jpg"))  # Remplacez "background.jpg" par votre image
        self.scene.addItem(self.pixmap_item)

        self.create_button("Bouton 1", 0.1, 0.1, 0.1, 0.05, self.button_clicked)
        self.create_button("Bouton 2", 0.2, 0.2, 0.1, 0.05, self.button_clicked)

    def create_button(self, text, x_ratio, y_ratio, width_ratio, height_ratio, function):
        button = QPushButton(text, self)
        # button.setStyleSheet("background-color: transparent;")
        button.clicked.connect(function)
        self.buttons[text] = (button, x_ratio, y_ratio, width_ratio, height_ratio)

    def button_clicked(self):
        sender = self.sender()
        sender.setText("Cliqué")

    def read_from_serial(self):
        data = self.serial_reader.read()
        if data is not None:
            print(data)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.resize(self.size())
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())
        self.pixmap_item.setPixmap(QPixmap("background.jpg").scaled(self.view.size()))  # Remplacez "background.jpg" par votre image
        menu_bar_height = self.menuBar().height()
        for button, x_ratio, y_ratio, width_ratio, height_ratio in self.buttons.values():
            button.move(int(x_ratio * self.width()), int(y_ratio * self.height()) + menu_bar_height)
            button.resize(int(width_ratio * self.width()), int(height_ratio * self.height()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
