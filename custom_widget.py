from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QMargins


class CustomWidget(QGraphicsWidget):
    def __init__(self, translator, pos, ratio, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.translator = translator
        self.labels = []
        self.buttons = []

        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(3, 3, 3, 3)  # Add this line to remove margins

        #ratio = x_ratio, y_ratio, width_ratio, height_ratio
        self.position = pos
        self.ratio = ratio



    def create_label(self, key,number = "", **kwargs):
        label = QLabel(self.translator.translate(key, number=number), **kwargs)
        label_proxy = QGraphicsProxyWidget(self)
        label_proxy.setWidget(label)

        label.setStyleSheet("background-color: transparent;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # New code


        font = label.font()  # New code
        label.setFont(font)  # New code

        self.layout.addItem(label_proxy)
        self.labels.append((label, label_proxy, key, number))


    def create_button(self, key, function=None):
        if function is None:
            function = lambda: None

        button = QPushButton(self.translator.translate(key))
        button.clicked.connect(function)
        button_proxy = QGraphicsProxyWidget(self)
        button_proxy.setWidget(button)

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # New code

        font = button.font()  # New code
        font.setPointSizeF(button.height()*self.ratio[1]*5)  # New code
        button.setFont(font)  # New code

        button.setContentsMargins(1, 1, 1, 1)
        button.setStyleSheet("QPushButton { padding-top: 2px; }")
        self.layout.addItem(button_proxy)
        self.buttons.append((button, button_proxy, key))  # Append the key for later language changes



    def paint(self, painter, option, widget):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 3, 3)
        painter.fillPath(path, QColor("#DDDDDD"))

    def change_language(self, lang):
        for label, _ , key, number in self.labels:
            label.setText(self.translator.translate(key,number=number))
        for button, _ , key in self.buttons:
            button.setText(self.translator.translate(key,number=number))

    def set_pos_size(self,width, height):
        self.resize(width*self.ratio[0], height*self.ratio[1])
        self.maximumSize = self.size()
        self.setPos(width*self.position[0], height*self.position[1])

        for label in self.labels:
            font = label[0].font()
            font.setPointSizeF(height*self.ratio[1]/10)
            label[0].setFont(font)

        for button in self.buttons:  # New code
            font = button[0].font()  # New code
            font.setPointSizeF(height*self.ratio[1]/10)  # New code
            button[0].setFont(font)  # New code