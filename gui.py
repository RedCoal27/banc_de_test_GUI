import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QAction, QMessageBox, QActionGroup
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPalette
from PyQt5.QtCore import Qt, QTimer
import serial
from serial.tools.list_ports import comports

class SerialReader:
    def __init__(self):
        self.ser = None
        self.set_com_port(self.get_available_com_ports()[0] if self.get_available_com_ports() else None)

    def get_available_com_ports(self):
        return [port.device for port in comports()]

    def set_com_port(self, port):
        if port is not None:
            try:
                self.ser = serial.Serial(port)
            except serial.SerialException:
                print(f"Impossible d'ouvrir le port {port}. Le programme continuera sans lire le port série.")
        else:
            QMessageBox.warning(None, "Avertissement", "Aucun port COM disponible.")

    def read(self):
        if self.ser is not None and self.ser.in_waiting:
            return self.ser.readline()
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_reader = SerialReader()

        self.buttons = {}

        self.init_ui()

    def init_ui(self):
        self.create_timer()
        self.create_menus()
        self.create_background_and_buttons()
        self.setWindowTitle("Interface PyQt5")
        self.setMinimumSize(400, 300)

    def create_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_serial)
        self.timer.start(1000)  # Lire toutes les secondes

    def create_menus(self):
        self.menuBar().addMenu(self.create_menu("Foo", ["Option 1", "Option 2"]))
        self.menuBar().addMenu(self.create_menu("Bar", ["Option 1", "Option 2"]))
        self.create_com_menu()

    def create_menu(self, menu_name, actions):
        menu = QMenu(menu_name, self)
        for action in actions:
            menu.addAction(action)
        return menu

    def create_com_menu(self):
        com_menu = QMenu("COM", self)
        action_group = QActionGroup(self)
        action_group.setExclusive(True)
        ports = self.serial_reader.get_available_com_ports()
        if ports:
            for port in ports:
                action = QAction(port, self)
                action.setCheckable(True)
                action.triggered.connect(lambda checked, port=port: self.serial_reader.set_com_port(port))
                action_group.addAction(action)
                com_menu.addAction(action)
                if self.serial_reader.ser is not None and self.serial_reader.ser.port == port:
                    action.setChecked(True)
        else:
            com_menu.addAction("Aucun disponible")
        self.menuBar().addMenu(com_menu)

    def create_background_and_buttons(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setCentralWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem(QPixmap("background.jpg"))  # Remplacez"background.jpg" par votre image
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
