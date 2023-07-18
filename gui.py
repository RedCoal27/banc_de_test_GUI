import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QAction, QMessageBox, QActionGroup
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette, QColor, QIcon,QGuiApplication, QPen
from PyQt5.QtCore import Qt, QTimer
import serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException
import json
import os

from translator import Translator
from serial_reader import SerialReader
from custom_widget import CustomWidget
from interlock import Interlock
from chamber import Chamber
from four_way import FourWay
from baratron import Baratron
from mfc import MFC
from line import Line
from gate import Gate
from circle import Circle
from convectron import Convectron
from pump import Pump
from motor_lift import MotorisedLift
from throttle_valve import ThrottleValve






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = Translator()
        self.translator.load_translations()
        self.serial_reader = SerialReader(self.translator)

        self.buttons = {}
        self.language_menu = None

        self.init_ui()
        QTimer.singleShot(0, self.resize_widgets)


    def init_ui(self):
        """
        Initializes the user interface by creating the timer, menus, background, and buttons.
        """
        self.create_timer()
        self.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Benchmark GUI")
        self.setMinimumSize(900, 600)
        self.view.resize(self.width(), self.height()-self.menuBar().height() - 2)

        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.setWindowIcon(QIcon(base_path + "\\images\\xfab.jpg"))
        self.resize(800, 600)


    def create_timer(self):
        """
        Creates a timer that reads from the serial port every second.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_menus(self):
        """
        Creates the COM and language menus.
        """
        self.com_menu = QMenu("COM", self)
        self.com_menu.aboutToShow.connect(self.update_com_menu)
        self.menuBar().addMenu(self.com_menu)

        self.language_menu = self.create_language_menu()
        self.menuBar().addMenu(self.language_menu)


    def create_menu(self, menu_name, actions):
        """
        Creates a menu with the given name and actions.

        Args:
            menu_name (str): The name of the menu.
            actions (list): A list of QAction objects to add to the menu.

        Returns:
            QMenu: The created menu.
        """
        menu = QMenu(menu_name, self)
        for action in actions:
            menu.addAction(action)
        return menu
    
    def update_com_menu(self):
        """
        Updates the COM menu with available ports.
        """
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
        """
        Creates the language menu.

        Returns:
            QMenu: The created language menu.
        """
        language_menu = QMenu(self.translator.translate("language"), self)
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        for language in self.translator.translations:
            action = QAction(self.translator.translate(language), self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, lang=language: self.change_language(lang))
            action_group.addAction(action)
            language_menu.addAction(action)
            if language == self.translator.current_language:
                action.setChecked(True)
        return language_menu

    def change_language(self, lang):
        """
        Changes the language of the GUI.

        Args:
            lang (str): The language to change to.
        """
        self.translator.current_language = lang
        self.language_menu.setTitle(self.translator.translate("language"))
        
        for key, button_tuple in self.buttons.items():
            button = button_tuple[0]
            button.setText(self.translator.translate(key))

        for item in self.scene.items():
            if isinstance(item, CustomWidget):
                item.change_language()




    def create_background_and_buttons(self):
        """
        Creates the background and custom widgets.
        """
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setCentralWidget(self.view)
        #décalage de la scene par rapport à la fenêtre
        self.create_lines()
        self.create_custom_widgets()
        self.scene.setBackgroundBrush(QBrush(QColor("#F5F5F5")))


    def create_lines(self):
        """
        Draws a line on the scene.
        """
        self.scene.addItem(Line(0.71, 0.27, 0.94, 0.27, "#4472C4")) # Numpro MFC1
        self.scene.addItem(Line(0.71, 0.27, 0.71, 0.41, "#4472C4")) # Numpro MFC1
        
        self.scene.addItem(Line(0.64, 0.41, 0.94, 0.41, "#4472C4")) # Numpro Final/ Numpro MFC2

        self.scene.addItem(Line(0.94, 0.22, 0.94, 0.41, "#4472C4")) # Numpro MFC2
        self.scene.addItem(Line(0.94, 0.22, 0.99, 0.22, "#4472C4")) # Numpro MFC2


        self.scene.addItem(Line(0.61, 0.15, 0.61, 0.3, "#4472C4")) # Numpro Vent
        self.scene.addItem(Line(0.61, 0.15, 0.99, 0.15, "#4472C4")) # Numpro Vent


        self.scene.addItem(Line(0.07, 0.45, 0.07, 0.83, "#4472C4")) # Turbo Pump RGA
        self.scene.addItem(Line(0.07, 0.45, 0.24, 0.45, "#4472C4")) # Turbo Pump RGA

        self.scene.addItem(Line(0.18, 0.48, 0.18, 0.83, "#4472C4")) # Turbo Pump CH
        self.scene.addItem(Line(0.18, 0.48, 0.24, 0.48, "#4472C4")) # Turbo Pump CH

        self.scene.addItem(Line(0.07, 0.83, 0.35, 0.83, "#4472C4")) # Turbo Pump CH/ Turbo Pump RGA

        self.scene.addItem(Line(0.64, 0.46, 0.71, 0.46, "#4472C4")) #Baratron/Chamber pressure
        self.scene.addItem(Line(0.71, 0.46, 0.71, 0.80, "#4472C4")) #Baratron/Chamber pressure
        self.scene.addItem(Line(0.71, 0.55, 0.76, 0.55, "#4472C4")) #Baratron1
        self.scene.addItem(Line(0.71, 0.68, 0.76, 0.68, "#4472C4")) #Baratron2
        self.scene.addItem(Line(0.71, 0.80, 0.76, 0.80, "#4472C4")) #Chamber pressure

        self.scene.addItem(Line(0.295, 0.64, 0.295, 0.86, "#4472C4")) #throttle valve/rouffing pump




    def create_custom_widgets(self):
        """
        Creates the custom widgets.
        """
        self.custom_widgets = {}
 
        self.custom_widgets["interlock"] = Interlock(self.translator, [0.05,0.1],"interlock")
        self.custom_widgets["Chamber"] = Chamber(self.translator, [0.24,0.3])

        self.custom_widgets["WL2"] = FourWay(self.translator, [0.24,0.12],"WL","2")
        self.custom_widgets["WL3"] = FourWay(self.translator, [0.365,0.12],"WL","3")
        self.custom_widgets["SV"] = FourWay(self.translator, [0.49,0.12],"SV")
        self.custom_widgets["throttle_valve"] = ThrottleValve(self.translator, [0.24,0.5],"throttle_valve" , "1")
        self.custom_widgets["motor_lift"] = MotorisedLift(self.translator, [0.37,0.5],"motor_lift")
        self.custom_widgets["WL1"] = FourWay(self.translator, [0.51,0.5],"WL","1")
        self.custom_widgets["baratron1"] = Baratron(self.translator, [0.76,0.5],"baratron1")
        self.custom_widgets["baratron2"] = Baratron(self.translator, [0.76,0.63],"baratron2")
        self.custom_widgets["MFC1"] = MFC(self.translator, [0.79,0.21],"MFC1")
        self.custom_widgets["MFC2"] = MFC(self.translator, [0.79,0.35],"MFC2")

        self.custom_widgets["chamber_pressure"] = Convectron(self.translator, [0.76,0.76],"chamber_pressure")

        self.custom_widgets["pump_pressure"] = Convectron(self.translator, [0.35,0.79],"pump_pressure")

        self.custom_widgets["turbo_pump_rga"] = Pump(self.translator, [0.02,0.6],"turbo_pump_rga")
        self.custom_widgets["turbo_pump_ch"] = Pump(self.translator, [0.13,0.6],"turbo_pump_ch")


        for key, custom_widget in self.custom_widgets.items():
            self.scene.addItem(custom_widget)


        self.custom_widgets["nupro_final"] = Gate([0.675,0.41], [0,-0.05],"nupro_final", 3, sens='vertical',parent=self)
        self.custom_widgets["nupro_MFC1"] = Gate([0.745,0.27], [0,-0.05],"nupro_mfc1", 1, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC2"] = Gate([0.745,0.41], [0,-0.05],"nupro_mfc2", 2, sens='vertical', parent=self)
        self.custom_widgets["nupro_vent"] = Gate([0.675,0.15], [0,-0.05],"nupro_vent", 4, sens='vertical', parent=self)

        self.custom_widgets["turbo_pump_rga_gate"] = Gate([0.07,0.5], [-0.04,0.0],"turbo_pump_rga_gate",16 , sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_rga_gate_p"] = Gate([0.07,0.75], [-0.04,0.0],"turbo_pump_rga_gate_p", 17, sens='horizontal', parent=self)

        self.custom_widgets["turbo_pump_ch_gate"] = Gate([0.18,0.55], [-0.04,0.0],"turbo_pump_ch_gate", 14, sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_ch_gate_p"] = Gate([0.18,0.75], [-0.04,0.0],"turbo_pump_ch_gate_p", 15, sens='horizontal', parent=self)

        self.custom_widgets["iso_chamber"] = Gate([0.295,0.79],[-0.04,-0.005],"iso_chamber", 25, sens='horizontal', parent=self)


    def read_from_serial(self):
        """
        Reads data from the serial port and prints it to the console.
        """
        self.serial_reader.send_data(1,0)   #read all DI
        data = self.serial_reader.wait_and_read_data(4)
        if data is not None and len(data) == 4:
            print(data)
            self.custom_widgets["WL2"].update_DI(data[0] & 16, data[0] & 32)
            self.custom_widgets["WL3"].update_DI(data[0] & 4, data[0] & 8)
            self.custom_widgets["SV"].update_DI(data[0] & 1, data[0] & 2)
            self.custom_widgets["WL1"].update_DI(data[0] & 64, data[0] & 128)



    def resize_widgets(self):
        """
        Resizes the view and buttons.

        This function is separated from resizeEvent so that it can be called on initialization.
        """
        screen_number = QApplication.desktop().screenNumber(self)
        screen = QGuiApplication.screens()[screen_number]
        dpi = screen.logicalDotsPerInch()
        scale_factor = dpi / 96.0 
        # Get current dimensions
        width = self.width()
        height = self.height()

        # Resize the view and scene
        self.view.resize(width, height - self.menuBar().height())
        self.scene.setSceneRect(0, 0, width, height)

        # Update background brush
        self.view.setBackgroundBrush(QBrush(QColor(0xf5f5f5)))

        # Resize and reposition buttons
        for button, x_ratio, y_ratio, width_ratio, height_ratio in self.buttons.values():
            button.move(x_ratio * width, y_ratio + self.menuBar().height())
            button.resize(width_ratio * width, height_ratio * height)

        # Resize custom widgets
        for item in self.scene.items():
            if isinstance(item, CustomWidget) or isinstance(item, Line) or isinstance(item, Circle):
                item.set_pos_size(width, height, scale_factor)



    def resizeEvent(self, event):
        """
        Resizes the view and buttons when the window is resized.

        Args:
            event (QResizeEvent): The resize event.
        """
        super().resizeEvent(event)
        self.resize_widgets()  # Call the new function here






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
