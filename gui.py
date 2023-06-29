import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton
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
        self.create_tabs()
        self.setCentralWidget(self.tabs)
        self.setWindowTitle("Interface PyQt5")

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_tabs(self):
        self.tabs = QTabWidget()

        self.tab1 = self.create_tab("Foo", "Bouton 1")
        self.tab2 = self.create_tab("Bar", "Bouton 2")

        self.tabs.addTab(self.tab1, "Foo")
        self.tabs.addTab(self.tab2, "Bar")

    def create_tab(self, tab_name, button_name):
        tab = QWidget()
        tab.layout = QVBoxLayout()

        button = QPushButton(button_name)
        tab.layout.addWidget(button)

        tab.setLayout(tab.layout)

        return tab

    def read_from_serial(self):
        data = self.serial_reader.read()
        if data is not None:
            print(data)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QPixmap("background.jpg")))  # Remplacez "background.jpg" par votre image
        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
