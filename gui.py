import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QAction, QMessageBox, QActionGroup
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer
import serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException
import json

from translator import Translator
from serial_reader import SerialReader
from custom_widget import CustomWidget
from four_way import FourWay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = Translator()
        self.translator.load_translations()
        self.serial_reader = SerialReader(self.translator)

        self.buttons = {}
        self.language_menu = None

        self.init_ui()


    def init_ui(self):
        self.create_timer()
        self.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Benchmark GUI")
        self.setMinimumSize(600, 400)
        self.setWindowIcon(QIcon("images/xfab.jpg"))

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_menus(self):
        self.com_menu = QMenu("COM", self)
        self.com_menu.aboutToShow.connect(self.update_com_menu)
        self.menuBar().addMenu(self.com_menu)

        self.language_menu = self.create_language_menu()
        self.menuBar().addMenu(self.language_menu)


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
            self.com_menu.addAction(self.translator.translate("none_available"))

    def create_language_menu(self):
        language_menu = QMenu(self.translator.translate("language"), self)
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        for language in ["en", "fr"]:
            action = QAction(self.translator.translate(language), self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, lang=language: self.change_language(lang))
            action_group.addAction(action)
            language_menu.addAction(action)
            if language == self.translator.current_language:
                action.setChecked(True)
        return language_menu

    def change_language(self, lang):
        self.translator.current_language = lang
        self.language_menu.setTitle(self.translator.translate("language"))
        for key, button_tuple in self.buttons.items():
            button = button_tuple[0]
            button.setText(self.translator.translate(key))

        for item in self.scene.items():
            if isinstance(item, CustomWidget):
                item.change_language(lang)

    def create_background_and_buttons(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setCentralWidget(self.view)

        self.create_custom_widgets()
        self.scene.setBackgroundBrush(QBrush(QColor("#F5F5F5")))



    def create_custom_widgets(self):
        self.custom_widgets = []
        self.custom_widgets.append(FourWay(self.translator, [0.1,0.1],"SV"))
        self.custom_widgets.append(FourWay(self.translator, [0.1,0.3],"WL","1"))
        self.custom_widgets.append(FourWay(self.translator, [0.1,0.5],"WL","2"))
        self.custom_widgets.append(FourWay(self.translator, [0.5,0.1],"WL","3"))


        for custom_widget in self.custom_widgets:
            self.scene.addItem(custom_widget)



    def read_from_serial(self):
        data = self.serial_reader.read()
        if data is not None:
            print(data)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.resize(self.size())
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())
        self.view.setBackgroundBrush(QBrush(QColor(0xf5f5f5)))
        menu_bar_height = self.menuBar().height()
        for button, x_ratio, y_ratio, width_ratio, height_ratio in self.buttons.values():
            button.move(int(x_ratio * self.width()), int(y_ratio * self.height()) + menu_bar_height)
            button.resize(int(width_ratio * self.width()), int(height_ratio * self.height()))

        # Resize custom widgets to be 10% of the scene size
        for item in self.scene.items():
            if isinstance(item, CustomWidget):
                item.set_pos_size(self.scene.width(), self.scene.height())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
