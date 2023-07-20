import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor, QIcon,QGuiApplication, QPen
from PyQt5.QtCore import Qt, QTimer
from serial.tools.list_ports import comports
import os

from internal.translator import Translator
from internal.serial_reader import *
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
from scene.roughing_pump import RoughingPump
from scene.motor_lift import MotorisedLift
from scene.throttle_valve import ThrottleValve
from scene.label import Label
from menu_manager import MenuManager
from internal.constant import *
from internal.logger import Logger



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = Translator()
        self.translator.load_translations()
        self.serial_reader = SerialReader(self.translator)

        self.custom_widgets = {}


        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menus()


        self.init_ui()
        QTimer.singleShot(0, self.resize_widgets)


        self.thread = SerialReaderThread(self.serial_reader, self.custom_widgets)  # type: ignore
        self.thread.start()




    def init_ui(self):
        """
        Initializes the user interface by creating the timer, menus, background, and buttons.
        """
        self.create_background_and_buttons()
        self.setWindowTitle("Benchmark GUI")

        #set the minimum size to 3/4 of the screen
        screen_size = QGuiApplication.primaryScreen().availableSize()
        self.setMinimumSize(int(screen_size.width()*3/4), int(screen_size.height()*3/4))

        self.view.resize(self.width(), self.height()-self.menuBar().height() - 2)

        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.setWindowIcon(QIcon(base_path + "\\images\\xfab.jpg"))
        self.resize(800, 600)




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
        self.scene.addItem(Line(0.71, 0.23, 0.94, 0.23, "#4472C4")) # Numpro MFC1
        self.scene.addItem(Line(0.71, 0.23, 0.71, 0.37, "#4472C4")) # Numpro MFC1
        
        self.scene.addItem(Line(0.64, 0.37, 0.94, 0.37, "#4472C4")) # Numpro Final/ Numpro MFC2

        self.scene.addItem(Line(0.94, 0.18, 0.94, 0.37, "#4472C4")) # Numpro MFC2
        self.scene.addItem(Line(0.94, 0.18, 0.99, 0.18, "#4472C4")) # Numpro MFC2


        self.scene.addItem(Line(0.61, 0.11, 0.61, 0.26, "#4472C4")) # Numpro Vent
        self.scene.addItem(Line(0.61, 0.11, 0.99, 0.11, "#4472C4")) # Numpro Vent


        self.scene.addItem(Line(0.07, 0.41, 0.07, 0.79, "#4472C4")) # Turbo Pump RGA
        self.scene.addItem(Line(0.07, 0.41, 0.24, 0.41, "#4472C4")) # Turbo Pump RGA

        self.scene.addItem(Line(0.18, 0.44, 0.18, 0.79, "#4472C4")) # Turbo Pump CH
        self.scene.addItem(Line(0.18, 0.44, 0.24, 0.44, "#4472C4")) # Turbo Pump CH

        self.scene.addItem(Line(0.07, 0.79, 0.38, 0.79, "#4472C4")) # Pump Pressure

        self.scene.addItem(Line(0.64, 0.42, 0.71, 0.42, "#4472C4")) #Baratron/Chamber pressure
        self.scene.addItem(Line(0.71, 0.42, 0.71, 0.76, "#4472C4")) #Baratron/Chamber pressure
        self.scene.addItem(Line(0.71, 0.51, 0.76, 0.51, "#4472C4")) #Baratron1
        self.scene.addItem(Line(0.71, 0.64, 0.76, 0.64, "#4472C4")) #Baratron2
        self.scene.addItem(Line(0.71, 0.76, 0.76, 0.76, "#4472C4")) #Chamber pressure

        self.scene.addItem(Line(0.295, 0.6, 0.295, 0.82, "#4472C4")) #throttle valve/rouffing pump




    def create_custom_widgets(self):
        """
        Creates the custom widgets.
        """
        self.custom_widgets = {}
 
        self.custom_widgets["interlock"] = Interlock(self.translator, [0.05,0.06],"interlock")
        self.custom_widgets["Chamber"] = Chamber(self.translator, [0.24,0.26])

        self.custom_widgets["WL2"] = FourWay(self, [0.24,0.03],9 ,"WL","2")
        self.custom_widgets["WL3"] = FourWay(self, [0.365,0.03],8 ,"WL","3")
        self.custom_widgets["SV"] = FourWay(self, [0.49,0.03], 7,"SV")
        self.custom_widgets["throttle_valve"] = ThrottleValve(self.translator, [0.24,0.46],"throttle_valve" , "1")
        self.custom_widgets["motor_lift"] = MotorisedLift(self.translator, [0.37,0.46],"motor_lift")
        self.custom_widgets["WL1"] = FourWay(self, [0.51,0.46],10 ,"WL","1")
        self.custom_widgets["baratron1"] = Baratron(self.translator, [0.76,0.46],"baratron1")
        self.custom_widgets["baratron2"] = Baratron(self.translator, [0.76,0.59],"baratron2")
        self.custom_widgets["MFC1"] = MFC(self.translator, [0.79,0.17],"MFC1")
        self.custom_widgets["MFC2"] = MFC(self.translator, [0.79,0.31],"MFC2")

        self.custom_widgets["chamber_pressure"] = Convectron(self.translator, [0.76,0.72],"chamber_pressure")

        self.custom_widgets["pump_pressure"] = Convectron(self.translator, [0.38,0.75],"pump_pressure")


        self.custom_widgets["turbo_pump_rga"] = Pump(self.translator, [0.02,0.53],"turbo_pump_rga")
        self.custom_widgets["turbo_pump_ch"] = Pump(self.translator, [0.13,0.53],"turbo_pump_ch")

        self.custom_widgets["roughing_pump"] = RoughingPump(self.translator, [0.245,0.82],"roughing_pump")

        for key, custom_widget in self.custom_widgets.items():
            self.scene.addItem(custom_widget)


        self.custom_widgets["nupro_final"] = Gate((0.675,0.37),(0,-0.05),"nupro_final", Cmd.nupro_final, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC1"] = Gate((0.745,0.23), (0,-0.05),"nupro_mfc1", Cmd.nupro_mfc1, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC2"] = Gate((0.745,0.37), (0,-0.05),"nupro_mfc2", Cmd.nupro_mfc2, sens='vertical', parent=self)
        self.custom_widgets["nupro_vent"] = Gate((0.675,0.11), (0,-0.05),"nupro_vent", Cmd.nupro_vent, sens='vertical', parent=self)

        self.custom_widgets["N2"] = Label((0.95,0.13),(0.02, 0.02),"N2", parent=self)

        self.custom_widgets["turbo_pump_rga_gate_ch"] = Gate((0.07,0.46), (-0.04,0.0),"turbo_pump_rga_gate", Cmd.turbo_pump_rga_gate, sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_rga_gate_p"] = Gate((0.07,0.73), (-0.04,0.0),"turbo_pump_rga_gate_p", Cmd.turbo_pump_rga_gate_p, sens='horizontal', parent=self)

        self.custom_widgets["turbo_pump_ch_gate_ch"] = Gate((0.18,0.48), (-0.04,0.0),"turbo_pump_ch_gate", Cmd.turbo_pump_ch_gate, sens='horizontal', parent=self)
        self.custom_widgets["turbo_pump_ch_gate_p"] = Gate((0.18,0.73), (-0.04,0.0),"turbo_pump_ch_gate_p", Cmd.turbo_pump_ch_gate_p, sens='horizontal', parent=self)

        self.custom_widgets["iso_chamber"] = Gate((0.295,0.75),(-0.04,-0.005),"iso_chamber", 25, sens='horizontal', parent=self)



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
