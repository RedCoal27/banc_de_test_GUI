from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QMargins

class CustomWidget(QGraphicsWidget):
    def __init__(self, translator, current_language, text, button_text, ratio, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.translator = translator
        self.current_language = current_language

        self.labels = []
        self.buttons = []

        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setLayout(self.layout)

        #ratio = x_ratio, y_ratio, width_ratio, height_ratio
        self.ratio = ratio

        self.create_labels()
        self.create_button(button_text)
        # self.set_pos_size(0, 0)


    def create_label(self, text):
        label = QLabel(self.translator.translate(text, self.current_language))
        label_proxy = QGraphicsProxyWidget(self)
        label_proxy.setWidget(label)

        self.layout.addItem(label_proxy)
        self.labels.append((label, label_proxy))

    def create_labels(self):
        self.create_label("a")
        self.create_label("b")
        self.create_label("c")

    def create_button(self, text, function=None):
        if function is None:
            function = lambda: None

        button = QPushButton(self.translator.translate(text, self.current_language))
        button.clicked.connect(function)
        button_proxy = QGraphicsProxyWidget(self)
        button_proxy.setWidget(button)

        self.layout.addItem(button_proxy)
        self.buttons.append((button, button_proxy))

    def create_buttons(self, buttons):
        for text, function in buttons:
            self.create_button(text, function)

    def paint(self, painter, option, widget):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 10, 10)
        painter.fillPath(path, QColor("#DDDDDD"))

    def change_language(self, lang):
        self.current_language = lang
        for label, _ in self.labels:
            label.setText(self.translator.translate(label.text(), self.current_language))
        for button, _ in self.buttons:
            button.setText(self.translator.translate(button.text(), self.current_language))


    def set_pos_size(self,width, height):
        self.resize(width*self.ratio[2], height*self.ratio[3])
        self.setPos(width*self.ratio[0], height*self.ratio[1])
