from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsTextItem, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QRectF, QMargins


class CustomWidget(QGraphicsWidget):
    def __init__(self, translator, pos: tuple[float,float], ratio: tuple[float,float], color:str, parent=None, police_size=8):
        """
        A custom widget that can contain labels and buttons.

        Args:
            translator: a translator object used for internationalization
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
        self.police_size = police_size

        self.layout = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(2, 4, 2, 4)  # Add this line to remove margins

        #ratio = x_ratio, y_ratio, width_ratio, height_ratio
        self.position = pos
        self.ratio = ratio



    def create_label(self, key, color="black", **kwargs):
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

        label.setStyleSheet(f"background-color: transparent;color: {color};")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # New code


        font = label.font()  # New code
        font.setPointSizeF(self.police_size)  # New code
        #set color text to white
        label.setFont(font)  # New code

        self.layout.addItem(label_proxy)
        self.labels.append((label, label_proxy, key, kwargs))


    def update_label(self, key, **kwargs):
        """
        Updates a label with the given key.

        Args:
            key (str): The translation key for the label.
        """
        # Loop over all labels
        for label, label_proxy, label_key, label_kwargs in self.labels:
            # If the key matches
            if label_key == key:
                # Update the state in kwargs
                for arg_name in kwargs:
                    label_kwargs[arg_name] = kwargs[arg_name]
                # Translate the new text and update the label
                label.setText(self.translator.translate(label_key, **label_kwargs))
                # Refresh the proxy widget
                label_proxy.setWidget(label)
                # We found the label, so we can break the loop
                break




    def create_button(self, key, function=None, **kwargs):
        """
        Creates a button with the given key and adds it to the widget.

        Args:
            key (str): The translation key for the button.
            function (function, optional): The function to be called when the button is clicked. Defaults to None.
        """
        if function is None:
            function = lambda: None

        button = QPushButton(self.translator.translate(key, **kwargs))
        button.clicked.connect(function)
        button_proxy = QGraphicsProxyWidget(self)
        button_proxy.setWidget(button)

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # New code

        font = button.font()  # New code
        font.setPointSizeF(self.police_size)  # New code
        button.setFont(font)  # New code

        button.setContentsMargins(1, 1, 1, 1)
        button.setStyleSheet("QPushButton { padding-top: 2px; }")
        self.layout.addItem(button_proxy)
        self.buttons.append((button, button_proxy, key, kwargs))  # Append the key for later language changes


    def update_button(self, key, state):
        """
        Updates a button with the given key.

        Args:
            key (str): The translation key for the button.
            state (str): The new state ("true" or "false").
        """
        # Loop over all buttons
        for button, button_proxy, button_key, kwargs in self.buttons:
            # If the key matches
            if button_key == key:
                # Update the state in kwargs
                kwargs['state'] = state
                # Translate the new text and update the button
                button.setText(self.translator.translate(button_key, **kwargs))
                # Refresh the proxy widget
                button_proxy.setWidget(button)
                # We found the button, so we can break the loop
                break

    def paint(self, painter, option, widget):
        """
        Paints the widget.

        Args:
            painter (QPainter): The painter object to use for painting.
            option: Unused.
            widget: Unused.
        """
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 6, 6)
        painter.fillPath(path, QColor(self.color))

    def change_language(self):
        """
        Changes the language of the widget.

        Args:
            lang (str): The language to change to.
        """
        for label, _ , key, kwargs in self.labels:
            label.setText(self.translator.translate(key,**kwargs))
        for button, _ , key, kwargs in self.buttons:
            button.setText(self.translator.translate(key,**kwargs))

    def set_pos_size(self,width, height,scale_factor):
        """
        Sets the position and size of the widget.

        Args:
            width (int): The width of the parent widget.
            height (int): The height of the parent widget.
        """


        for label in self.labels:
            font = label[0].font()
            font.setPointSizeF(self.police_size)  # New code
            label[0].setFont(font)

        for button in self.buttons:  # New code
            font = button[0].font()  # New code
            font.setPointSizeF(self.police_size)  # New code
            button[0].setFont(font)  # New code
            #change button size
            button[0].setFixedWidth(int(width*self.ratio[0]))


        self.resize(width*self.ratio[0], height*self.ratio[1])
        self.maximumSize = self.size()
        self.setPos(width*self.position[0], height*self.position[1])
