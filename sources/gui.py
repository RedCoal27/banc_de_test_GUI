import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor, QIcon,QGuiApplication, QPen
from PyQt5.QtCore import Qt, QTimer
from serial.tools.list_ports import comports
import os

from internal.translator import Translator
from internal.serial_reader import *
from internal.custom_widget import CustomWidget

from scene.auto import Auto
from scene.interlock import Interlock
from scene.chamber import Chamber
from scene.chamber_label import ChamberLabel
from scene.four_way import FourWay
from scene.baratron import Baratron
from scene.mfc import MFC
from scene.line import Line
from scene.gate import Gate
from scene.gate_ch import GateCH
from scene.circle import Circle
from scene.jauge_pression import JaugePression
from scene.turbo_pump import TurboPump
from scene.roughing_pump import RoughingPump
from scene.motor_lift import MotorisedLift
from scene.throttle_valve import ThrottleValve
from scene.label import Label
from scene.ion_gauge import IonGauge
from internal.menu_manager import MenuManager
from internal.constant import *
from internal.logger import Logger
from internal.config import Config
from internal.recipes import Recipes


from internal.rs485 import RS485


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = Config(self)
        self.translator = Translator(self.config)
        self.translator.load_translations()
        self.recipes = Recipes(self)
        

        self.serial_reader = SerialReader(self)
        self.RS485 = RS485(self)

        self.auto_mode = False
        
        self.custom_widgets = {}

        self.icon = None

        self.menu_manager = MenuManager(self)

        self.init_ui()



        QTimer.singleShot(0, self.resize_widgets)


        self.thread = SerialReaderThread(self)  # type: ignore
        self.thread.start()



    def show_error_message(self, message):
        QMessageBox.warning(self, self.translator.translate("warning"),message)

    def set_value(self, key, value):
        """
        Sets the value of a custom widget.

        Args:
            key (str): The key of the custom widget.
            value (float): The new value.
        """
        print(f"Setting value of {key} to {value}")
        self.custom_widgets[key].set_value(value)


    def init_ui(self):
        """
        Initializes the user interface by creating the timer, menus, background, and buttons.
        """
        self.menu_manager.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Benchmark GUI")

        #set the minimum size to 3/4 of the screen
        screen_size = QGuiApplication.primaryScreen().availableSize()
        self.setMinimumSize(int(screen_size.width()*8.8/10), int(screen_size.height()*8.8/10))
        self.view.resize(self.width(), self.height()-self.menuBar().height() - 2)

        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.icon = QIcon(base_path + "\\images\\xfab.jpg")

        self.setWindowIcon(self.icon)

        self.showMaximized()

        self.menu_manager.change_font_size(self.config["gui"]["font_size"])





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
        self.scene.addItem(Line(0.71, 0.21, 0.94, 0.21, "#4472C4")) # Numpro MFC1
        self.scene.addItem(Line(0.71, 0.21, 0.71, 0.35, "#4472C4")) # Numpro MFC1
        
        self.scene.addItem(Line(0.64, 0.35, 0.94, 0.35, "#4472C4")) # Numpro Final/ Numpro MFC2

        self.scene.addItem(Line(0.94, 0.16, 0.94, 0.35, "#4472C4")) # Numpro MFC2
        self.scene.addItem(Line(0.94, 0.16, 0.99, 0.16, "#4472C4")) # Numpro MFC2


        self.scene.addItem(Line(0.61, 0.09, 0.61, 0.24, "#4472C4")) # Numpro Vent
        self.scene.addItem(Line(0.61, 0.09, 0.99, 0.09, "#4472C4")) # Numpro Vent


        self.scene.addItem(Line(0.07, 0.28, 0.07, 0.77, "#4472C4")) # Turbo Pump RGA
        self.scene.addItem(Line(0.07, 0.28, 0.24, 0.28, "#4472C4")) # Turbo Pump RGA

        self.scene.addItem(Line(0.18, 0.35, 0.18, 0.77, "#4472C4")) # Turbo Pump CH
        self.scene.addItem(Line(0.18, 0.35, 0.24, 0.35, "#4472C4")) # Turbo Pump CH

        self.scene.addItem(Line(0.07, 0.77, 0.38, 0.77, "#4472C4")) # Pump Pressure

        self.scene.addItem(Line(0.64, 0.4, 0.71, 0.4, "#4472C4")) #Baratron/Chamber pressure
        self.scene.addItem(Line(0.71, 0.4, 0.71, 0.88, "#4472C4")) #Baratron/Chamber pressure

        self.scene.addItem(Line(0.71, 0.49, 0.76, 0.49, "#4472C4")) #Baratron1
        self.scene.addItem(Line(0.71, 0.62, 0.76, 0.62, "#4472C4")) #Baratron2
        self.scene.addItem(Line(0.71, 0.74, 0.76, 0.74, "#4472C4")) #Chamber pressure
        self.scene.addItem(Line(0.71, 0.88, 0.76, 0.88, "#4472C4")) #Chamber pressure

        self.scene.addItem(Line(0.295, 0.58, 0.295, 0.8, "#4472C4")) #throttle valve/rouffing pump




    def create_custom_widgets(self):
        """
        Creates the custom widgets.
        """
        self.custom_widgets = {}
 
        self.custom_widgets["auto"] = Auto([0.05,0.01], self)
        self.custom_widgets["interlock"] = Interlock([0.05,0.1], "interlock", self)
        self.custom_widgets["chamber"] = Chamber([0.24,0.24], self)
        self.custom_widgets["chamber_label"] = ChamberLabel([0.24,0.24], self)


        self.custom_widgets["WL2"] = FourWay([0.24,0.01], Cmd.WL2, "WL", number="2", parent=self)
        self.custom_widgets["WL3"] = FourWay([0.365,0.01], Cmd.WL3, "WL", number="3", parent=self)
        self.custom_widgets["SV"] = FourWay([0.49,0.01], Cmd.SV, "SV", parent=self)
        self.custom_widgets["throttle_valve"] = ThrottleValve([0.24,0.44], "throttle_valve", parent=self)
        self.custom_widgets["motor_lift"] = MotorisedLift([0.37,0.44], "motor_lift", parent=self)
        self.custom_widgets["WL1"] = FourWay([0.51,0.44] , Cmd.WL1, "WL", number="1", parent=self)
        self.custom_widgets["baratron1"] = Baratron([0.76,0.44], "baratron1", parent=self)
        self.custom_widgets["baratron2"] = Baratron([0.76,0.57], "baratron2", parent=self)
        self.custom_widgets["MFC1"] = MFC([0.79,0.15], Cmd.MFC1, "MFC1", self)
        self.custom_widgets["MFC2"] = MFC([0.79,0.29], Cmd.MFC2, "MFC2", self)

        self.custom_widgets["chamber_pressure"] = JaugePression([0.76,0.7], "chamber_pressure", parent=self)

        self.custom_widgets["ion_gauge"] = IonGauge([0.76,0.83], "ion_gauge", parent=self)

        self.custom_widgets["pump_pressure"] = JaugePression([0.38,0.73], "pump_pressure", parent=self)

        self.custom_widgets["turbo_pump_rga"] = TurboPump([0.02,0.51], Cmd.TurboRGA, "turbo_pump_rga", parent=self)
        self.custom_widgets["turbo_pump_ch"] = TurboPump([0.13,0.51], Cmd.TurboCH, "turbo_pump_ch", parent=self)

        self.custom_widgets["roughing_pump"] = RoughingPump([0.245,0.8], Cmd.RoughingPump, "roughing_pump", parent=self)


        for key, custom_widget in self.custom_widgets.items():
            self.scene.addItem(custom_widget)

        self.custom_widgets["nupro_final"] = Gate((0.675,0.35), (0,-0.05), "nupro_final", Cmd.nupro_final, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC1"] = Gate((0.745,0.21), (0,-0.05), "nupro_mfc1", Cmd.nupro_mfc1, sens='vertical', parent=self)
        self.custom_widgets["nupro_MFC2"] = Gate((0.745,0.35), (0,-0.05), "nupro_mfc2", Cmd.nupro_mfc2, sens='vertical', parent=self)
        self.custom_widgets["nupro_vent"] = Gate((0.675,0.09), (0,-0.05), "nupro_vent", Cmd.nupro_vent, sens='vertical', parent=self)

        self.custom_widgets["N2"] = Label((0.95,0.11),(0.02, 0.02),"N2", parent=self)

        self.custom_widgets["iso_rga_ch"] = Gate((0.07,0.40), (-0.04,0.0),"iso_rga", Cmd.iso_rga, sens='horizontal', parent=self, color="#FD6801")
        self.custom_widgets["iso_rga_pump"] = Gate((0.07,0.71), (-0.04,0.0),"iso_rga_pump", Cmd.iso_rga_pump, sens='horizontal', parent=self, color="#FD6801")
        self.custom_widgets["iso_turbo"] = Gate((0.18,0.71), (-0.04,0.0),"iso_turbo", Cmd.iso_turbo, sens='horizontal', parent=self, color="#FD6801")

        self.custom_widgets["turbo_pump_gate"] = GateCH((0.18,0.43), (-0.04,0.0),"turbo_pump_gate", Cmd.RGAGate, sens='horizontal', parent=self, color="#FD6801")

        self.custom_widgets["iso_chamber"] = Gate((0.295,0.73),(-0.04,-0.005),"iso_chamber", Cmd.iso_chamber, sens='horizontal', parent=self, color="#FD6801")



    def update_AI(self):#certains éléments comme les lignes nécéssit d'être tracé uniquement depuis le thread principale
        self.custom_widgets["turbo_pump_gate"].update_sensor_line()


    def resize_widgets(self):
        """
        Resizes the view and buttons.

        This function is separated from resizeEvent so that it can be called on initialization.
        """
        screen_number = QApplication.desktop().screenNumber(self)
        screen = QGuiApplication.screens()[screen_number]

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
                item.set_pos_size(width, height)



    def resizeEvent(self, event):
        """
        Resizes the view and buttons when the window is resized.

        Args:
            event (QResizeEvent): The resize event.
        """
        super().resizeEvent(event)
        self.resize_widgets()  # Call the new function here



if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False) 
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False) 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
