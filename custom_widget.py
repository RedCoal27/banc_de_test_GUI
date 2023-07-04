from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QMargins


class CustomWidget(QGraphicsWidget):
    def __init__(self, translator, pos, ratio, color, parent=None):
        """
        A custom widget that can contain labels and buttons.

        Args:
            translator (QTranslator): A translator object used to translate text.
            pos (tuple): A tuple containing the x and y position of the widget as a ratio of the parent widget's width and height.
            ratio (tuple): A tuple containing the x and y ratios of the widget's width and height relative to the parent widget's width and height.
            color (str): The background color of the widget in hexadecimal format (e.g. "#FFFFFF").
            parent (QGraphicsWidget, optional): The parent widget. Defaults to None.
        """
        super(CustomWidget, self).__init__(parent)
        self.translator = translator
        self.labels = []
        self.buttons = []
        self.color = color

        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(3, 3, 3, 3)  # Add this line to remove margins

        #ratio = x_ratio, y_ratio, width_ratio, height_ratio
        self.position = pos
        self.ratio = ratio



    def create_label(self, key, **kwargs):
        """
        Creates a label with the given key and adds it to the widget.

        Args:
            key (str): The translation key for the label.
            **kwargs: Additional keyword arguments to be passed to the QLabel constructor and for translation.
        """
        label_translate = {}
        for arg_name in ['alignment', 'indent', 'margin', 'text', 'wordWrap']: #argument du QLabel possible
            if arg_name in kwargs:
                label_translate[arg_name] = kwargs.pop(arg_name)


        label = QLabel(self.translator.translate(key, **kwargs), **label_translate)
        label_proxy = QGraphicsProxyWidget(self)
        label_proxy.setWidget(label)

        label.setStyleSheet("background-color: transparent;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # New code


        font = label.font()  # New code
        label.setFont(font)  # New code

        self.layout.addItem(label_proxy)
        self.labels.append((label, label_proxy, key, kwargs))


    def create_button(self, key, function=None):
        """
        Creates a button with the given key and adds it to the widget.

        Args:
            key (str): The translation key for the button.
            function (function, optional): The function to be called when the button is clicked. Defaults to None.
        """
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
        """
        Paints the widget.

        Args:
            painter (QPainter): The painter object to use for painting.
            option: Unused.
            widget: Unused.
        """
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 3, 3)
        painter.fillPath(path, QColor(self.color))

    def change_language(self):
        """
        Changes the language of the widget.

        Args:
            lang (str): The language to change to.
        """
        for label, _ , key, kwargs in self.labels:
            label.setText(self.translator.translate(key,**kwargs))
        for button, _ , key in self.buttons:
            button.setText(self.translator.translate(key,**kwargs))

    def set_pos_size(self,width, height):
        """
        Sets the position and size of the widget.

        Args:
            width (int): The width of the parent widget.
            height (int): The height of the parent widget.
        """
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