import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette
from PyQt5.QtCore import Qt, QTimer
import serial

class SerialReader:
    def __init__(self, port):
        try:
            self.ser = serial.Serial(port)
        except serial.SerialException:
            print(f"Impossible d'ouvrir le port {port}. Le programme continuera sans lire le port série.")
            self.ser = None

    def read(self):
        if self.ser is not None and self.ser.in_waiting:
            return self.ser.readline()
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_reader = SerialReader('COM3')  # Remplacez 'COM3' par le port série que vous utilisez

        self.init_ui()

    def init_ui(self):
        self.create_timer()
        self.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Interface PyQt5")

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_menus(self):
        self.menuBar().addMenu(self.create_menu("Foo"))
        self.menuBar().addMenu(self.create_menu("Bar"))

    def create_menu(self, menu_name):
        menu = QMenu(menu_name, self)
        menu.addAction("Option 1")
        menu.addAction("Option 2")
        return menu

    def create_background_and_buttons(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        pixmap = QPixmap("background.jpg")  # Remplacez "background.jpg" par votre image
        self.scene.addPixmap(pixmap)

        self.button1 = QPushButton("Bouton 1", self)
        self.button1.setStyleSheet("background-color: transparent;")
        self.button1.move(50, 50)

        self.button2 = QPushButton("Bouton 2", self)
        self.button2.setStyleSheet("background-color: transparent;")
        self.button2.move(100, 100)

    def read_from_serial(self):
        data = self.serial_reader.read()
        if data is not None:
            print(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
