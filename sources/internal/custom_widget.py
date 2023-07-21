from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel, QSizePolicy, QLineEdit, QHBoxLayout, QWidget, QSpinBox
from PyQt5.QtGui import QPainterPath, QColor, QIntValidator
from PyQt5.QtCore import Qt, QSize

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
        self.spin_boxes = []
        self.unit_labels = []
        self.color = color
        self.police_size = police_size

        self.layout = QGraphicsLinearLayout(Qt.Orientation.Vertical)  # type: ignore
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
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setContentsMargins(1, 1, 1, 1)  # Set margins for the units QLabel

        font = label.font()
        font.setPointSizeF(self.police_size)
        #set color text to white
        label.setFont(font)
    
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

    def create_label_with_spin_box(self, key, initial_value=0, min_value = 0,max_value=1000 , color="black", units="", function=None, **kwargs):
        """
        Creates a QLabel and a QSpinBox, and adds them to the widget in a QHBoxLayout.

        Args:
            key (str): The translation key for the label.
            initial_value (int, optional): The initial value of the QSpinBox. Defaults to 0.
            units (str, optional): The units to display after the QSpinBox. Defaults to "".
            function (function, optional): The function to be called when the QSpinBox is edited and confirmed. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the QLabel constructor and for translation.
        """
        label_translate = {}
        for arg_name in ['alignment', 'indent', 'margin', 'text', 'wordWrap']:  # argument du QLabel possible
            if arg_name in kwargs:
                label_translate[arg_name] = kwargs.pop(arg_name)

        label = QLabel(self.translator.translate(key, **kwargs), **label_translate)
        label.setStyleSheet(f"background-color: transparent;color: {color};")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setContentsMargins(1, 1, 0, 1)  # Set margins for the units QLabel

        font = label.font()
        font.setPointSizeF(self.police_size)
        label.setFont(font)

        spin_box = QSpinBox()
    
        spin_box.setRange(min_value, max_value)  # Set the allowed range of values
        spin_box.setValue(initial_value)
        spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spin_box.setFixedSize(QSize(30, 20))  # Set a fixed size
        spin_box.setStyleSheet("QSpinBox { font-size: " + str(self.police_size) + "pt; }")
        spin_box.setContentsMargins(0, 0, 0, 0)  # Remove margins for the QSpinBox

        font = spin_box.font()
        font.setPointSizeF(self.police_size)
        spin_box.setFont(font)

        # If a function was provided, connect the QSpinBox's editingFinished signal to it
        if function is not None:
            def on_editing_finished():
                function(spin_box)
            spin_box.editingFinished.connect(on_editing_finished)

        unit_label = QLabel(units)
        unit_label.setStyleSheet("background-color: transparent;color: black;")  # Adjust color as needed
        unit_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = unit_label.font()
        font.setPointSizeF(self.police_size)
        unit_label.setFont(font)
        unit_label.setContentsMargins(1, 1, 0, 1)  # Set margins for the units QLabel


        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)  # Set smaller margins
        hbox.addWidget(label)
        hbox.addWidget(spin_box)
        hbox.addWidget(unit_label)
        hbox.addStretch(1)  # Add a stretchable space

        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")  # Set transparent background
        widget.setLayout(hbox)

        widget_proxy = QGraphicsProxyWidget(self)
        widget_proxy.setWidget(widget)

        self.layout.addItem(widget_proxy)

        self.labels.append((label, widget_proxy, key, kwargs))  # Append the key for later language changes
        self.spin_boxes.append((spin_box, key, max_value, kwargs))  # Append the initial value and kwargs for later language changes
        self.unit_labels.append((unit_label, units, kwargs))  # Append the units and kwargs for later language changes


    def update_spin_box(self, key, max_value):
        """
        Updates a spin box with the given key.

        Args:
            key (str): The translation key for the spin box.
            max_value (int): The new maximum value.
        """
        # Loop over all spin boxes
        for spin_box, spin_box_key, _, spin_box_kwargs in self.spin_boxes:
            # If the key matches
            if spin_box_key == key:
                # Update the state in kwargs
                spin_box_kwargs['max_value'] = max_value
                # Translate the new text and update the spin box
                spin_box.setRange(0, max_value)
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

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = button.font()
        font.setPointSizeF(self.police_size)
        button.setFont(font)

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
        for spin_box, initial_value, kwargs in self.spin_boxes:
            spin_box.setValue(self.translator.translate(initial_value,**kwargs))  # Update the value of the QSpinBox
        for unit_label, units, kwargs in self.unit_labels:
            unit_label.setText(self.translator.translate(units,**kwargs))  # Update the text of the unit QLabel



    def set_pos_size(self,width, height,scale_factor):
        """
        Sets the position and size of the widget.

        Args:
            width (int): The width of the parent widget.
            height (int): The height of the parent widget.
        """


        for label in self.labels:
            font = label[0].font()
            font.setPointSizeF(self.police_size)
            label[0].setFont(font)

        for button in self.buttons:
            font = button[0].font()
            font.setPointSizeF(self.police_size)
            button[0].setFont(font)
            #change button size
            button[0].setFixedWidth(int(width*self.ratio[0]))

        for spin_box in self.spin_boxes:
            spin_box[0].setStyleSheet("QSpinBox { font-size: " + str(self.police_size-1) + "pt; }")
            spin_box[0].setFixedWidth(int(width*self.ratio[0]/3.5))  # Adjust the 4 as needed
            spin_box[0].setFixedHeight(int(height*self.ratio[1]/6))  # Adjust the 4 as needed

        for unit_label in self.unit_labels:
            font = unit_label[0].font()
            font.setPointSizeF(self.police_size)
            unit_label[0].setFont(font)



        self.resize(width*self.ratio[0], height*self.ratio[1])
        self.maximumSize = self.size()
        self.setPos(width*self.position[0], height*self.position[1])
