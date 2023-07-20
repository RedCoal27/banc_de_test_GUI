import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor, QIcon,QGuiApplication, QPen
from PyQt5.QtCore import Qt, QTimer
from serial.tools.list_ports import comports
import os

from internal.translator import Translator
from internal.serial_reader import SerialReader
from internal.custom_widget import CustomWidget
from scene.interlock import Interlock
from scene.chamber import Chamber
from scene.four_way import FourWay
from scene.baratron import Baratron
from scene.mfc import MFC
from scene.line import Line
from scene.gate import Gate
from scene.circle import Circle
from scene.convectron import Convectron
from scene.pump import Pump
from scene.motor_lift import MotorisedLift
from scene.throttle_valve import ThrottleValve
from scene.label import Label

from menu_manager import MenuManager
from internal.constante import *
from internal.logger import Logger



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = Translator()
        self.translator.load_translations()
        self.serial_reader = SerialReader(self.translator)

        self.buttons = {}

        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menus()


        self.init_ui()
        QTimer.singleShot(0, self.resize_widgets)



    def init_ui(self):
        """
        Initializes the user interface by creating the timer, menus, background, and buttons.
        """
        self.create_timer()
        self.create_background_and_buttons()
        self.setWindowTitle("Benchmark GUI")

        #set the minimum size to 3/4 of the screen
        screen_size = QGuiApplication.primaryScreen().availableSize()
        self.setMinimumSize(int(screen_size.width()*3/4), int(screen_size.height()*3/4))

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




    def create_background_and_buttons(self):
        """
        Creates the background and custom widgets.
        """
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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

        self.custom_widgets["WL2"] = FourWay(self, [0.24,0.07],9 ,"WL","2")
        self.custom_widgets["WL3"] = FourWay(self, [0.365,0.07],8 ,"WL","3")
        self.custom_widgets["SV"] = FourWay(self, [0.49,0.07], 7,"SV")
        self.custom_widgets["throttle_valve"] = ThrottleValve(self.translator, [0.24,0.5],"throttle_valve" , "1")
        self.custom_widgets["motor_lift"] = MotorisedLift(self.translator, [0.37,0.5],"motor_lift")
        self.custom_widgets["WL1"] = FourWay(self, [0.51,0.5],10 ,"WL","1")
        self.custom_widgets["baratron1"] = Baratron(self.translator, [0.76,0.5],"baratron1")
        self.custom_widgets["baratron2"] = Baratron(self.translator, [0.76,0.63],"baratron2")
        self.custom_widgets["MFC1"] = MFC(self.translator, [0.79,0.21],"MFC1")
        self.custom_widgets["MFC2"] = MFC(self.translator, [0.79,0.35],"MFC2")

        self.custom_widgets["chamber_pressure"] = Convectron(self.translator, [0.76,0.76],"chamber_pressure")

        self.custom_widgets["pump_pressure"] = Convectron(self.translator, [0.35,0.79],"pump_pressure")

        self.custom_widgets["turbo_pump_rga"] = Pump(self.translator, [0.02,0.57],"turbo_pump_rga")
        self.custom_widgets["turbo_pump_ch"] = Pump(self.translator, [0.13,0.57],"turbo_pump_ch")


        for key, custom_widget in self.custom_widgets.items():
            self.scene.addItem(custom_widget)


        self.custom_widgets["nupro_final"] = Gate((0.675,0.41),(0,-0.05),"nupro_final", Cmd.nupro_final, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC1"] = Gate((0.745,0.27), (0,-0.05),"nupro_mfc1", Cmd.nupro_mfc1, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC2"] = Gate((0.745,0.41), (0,-0.05),"nupro_mfc2", Cmd.nupro_mfc2, sens='vertical', parent=self)
        self.custom_widgets["nupro_vent"] = Gate((0.675,0.15), (0,-0.05),"nupro_vent", Cmd.nupro_vent, sens='vertical', parent=self)

        self.custom_widgets["N2"] = Label((0.95,0.17),(0.02, 0.02),"N2", parent=self)

        self.custom_widgets["turbo_pump_rga_gate_ch"] = Gate((0.07,0.5), (-0.04,0.0),"turbo_pump_rga_gate", Cmd.turbo_pump_rga_gate, sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_rga_gate_p"] = Gate((0.07,0.77), (-0.04,0.0),"turbo_pump_rga_gate_p", Cmd.turbo_pump_rga_gate_p, sens='horizontal', parent=self)

        self.custom_widgets["turbo_pump_ch_gate_ch"] = Gate((0.18,0.52), (-0.04,0.0),"turbo_pump_ch_gate", Cmd.turbo_pump_ch_gate, sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_ch_gate_p"] = Gate((0.18,0.77), (-0.04,0.0),"turbo_pump_ch_gate_p", Cmd.turbo_pump_ch_gate_p, sens='horizontal', parent=self)

        self.custom_widgets["iso_chamber"] = Gate((0.295,0.79),(-0.04,-0.005),"iso_chamber", 25, sens='horizontal', parent=self)


    def read_from_serial(self):
        """
        Reads data from the serial port and prints it to the console.
        """
        self.serial_reader.send_data(1,0)   #read all DI
        data = self.serial_reader.wait_and_read_data(4)
        if data is not None and len(data) == 4:
            # print(data)
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
