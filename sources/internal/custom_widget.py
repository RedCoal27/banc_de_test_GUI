from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsProxyWidget, QPushButton, QGraphicsLinearLayout, QLabel, QSizePolicy, QHBoxLayout, QWidget, QSpinBox, QComboBox
from PyQt5.QtGui import QPainterPath, QColor, QBrush, QPainter, QPixmap
from PyQt5.QtCore import Qt, QSize






class CustomWidget(QGraphicsWidget):
    """
    Description:
    Classe CustomWidget, un widget personnalisé pouvant contenir des étiquettes et des boutons.

    Methods:
        __init__(self, translator, pos: tuple[float,float], ratio: tuple[float,float], color:str, font_size=8):
            Constructeur de la classe CustomWidget.

        create_label(self, key, color="black", **kwargs):
            Crée une étiquette avec la clé donnée et l'ajoute au widget.

        update_label(self, key, **kwargs):
            Met à jour une étiquette avec la clé donnée.

        create_label_with_spin_box(self, key, initial_value=0, min_value=0, max_value=1000, color="black", unit="", function=None, **kwargs):
            Crée une étiquette avec une boîte à filer et l'ajoute au widget.

        update_spin_box(self, key, max_value):
            Met à jour une boîte à filer avec la clé donnée.

        create_button(self, key, function=None, **kwargs):
            Crée un bouton avec la clé donnée et l'ajoute au widget.

        update_button(self, key, state):
            Met à jour un bouton avec la clé donnée.

        create_label_with_indicator(self, key, color="black", **kwargs):
            Crée une étiquette avec un indicateur et l'ajoute au widget.

        update_indicator(self, indicator, key, state):
            Met à jour un indicateur avec la clé et l'état donnés.

        create_label_with_combo_box_and_button(self, key, combo_items=[], button_function=None, color="black", button_key="", **kwargs):
            Crée une étiquette avec une boîte de combinaison et un bouton et les ajoute au widget.

        paint(self, painter, option, widget):
            Peint le widget.

        change_language(self):
            Change la langue du widget.

        set_font_size(self, size):
            Modifie la taille de police du widget.

        set_pos_size(self, width, height):
            Définit la position et la taille du widget.
    """
    def __init__(self, translator, pos: tuple[float,float], ratio: tuple[float,float], color: str, font_size=8):
        """
        Constructeur de la classe CustomWidget.

        Args:
            translator: Un objet traducteur utilisé pour l'internationalisation.
            pos (tuple): Un tuple contenant la position x et y du widget en tant que ratio de la largeur et de la hauteur du widget parent.
            ratio (tuple): Un tuple contenant les rapports x et y de la largeur et de la hauteur du widget par rapport à la largeur et à la hauteur du widget parent.
            color (str): La couleur de fond du widget au format hexadécimal (par exemple, "#FFFFFF").
            font_size (int): La taille de la police. Par défaut, 8.
        """
        super(CustomWidget, self).__init__(None)
        self.translator = translator
        self.labels = []
        self.buttons = []
        self.spin_boxes = []
        self.unit_labels = []
        self.indicators = []  # Create a new list for indicators
        self.combo_boxes = []
        self.color = color
        self.font_size = font_size

        self.layout = QGraphicsLinearLayout(Qt.Orientation.Vertical)  # type: ignore
        self.setLayout(self.layout)

        self.layout.setSpacing(0)  # Set spacing to 0
        self.layout.setContentsMargins(2, 4, 2, 4)  # Add this line to remove margins


        #ratio = x_ratio, y_ratio, width_ratio, height_ratio
        self.position = pos
        self.ratio = ratio



    def create_label(self, key, color="black", **kwargs):
        """
        Crée une étiquette avec la clé donnée et l'ajoute au widget.

        Args:
            key (str) : Clé de traduction pour l'étiquette.
            color (str) : Couleur du texte de l'étiquette (par défaut : "black").
            **kwargs : Arguments supplémentaires pour le constructeur QLabel et pour la traduction.
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
        label.setContentsMargins(1, 0, 1, 0)  # Set margins for the unit QLabel

        font = label.font()
        font.setPointSizeF(self.font_size)
        #set color text to white
        label.setFont(font)
    
        self.layout.addItem(label_proxy)
        self.labels.append((label, label_proxy, key, kwargs))



    def update_label(self, key, **kwargs):
        """
        Met à jour une étiquette avec la clé donnée.

        Args:
            key (str) : Clé de traduction pour l'étiquette.
            **kwargs : Arguments supplémentaires pour la traduction.
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
                # We found the label, so we can break the loop
                break

    def create_label_with_spin_box(self, key, initial_value=0, min_value = 0,max_value=1000 , color="black", unit="", function=None, **kwargs):
        """
        Crée une étiquette avec une boîte à filer (spin box) et l'ajoute au widget.

        Args:
            key (str) : Clé de traduction pour l'étiquette.
            initial_value (int) : Valeur initiale de la boîte à filer.
            min_value (int) : Valeur minimale de la boîte à filer.
            max_value (int) : Valeur maximale de la boîte à filer.
            color (str) : Couleur du texte de l'étiquette.
            unit (str) : Unité à afficher après la boîte à filer.
            function (fonction) : Fonction à appeler lorsque la valeur de la boîte à filer est modifiée.
            **kwargs : Arguments supplémentaires pour le constructeur QLabel et pour la traduction.
        """
        label_translate = {}
        for arg_name in ['alignment', 'indent', 'margin', 'text', 'wordWrap']:  # argument du QLabel possible
            if arg_name in kwargs:
                label_translate[arg_name] = kwargs.pop(arg_name)

        label = QLabel(self.translator.translate(key, **kwargs), **label_translate)
        label.setStyleSheet(f"background-color: transparent;color: {color};")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setContentsMargins(1, 1, 0, 1)  # Set margins for the unit QLabel

        font = label.font()
        font.setPointSizeF(self.font_size)
        label.setFont(font)

        spin_box = QSpinBox()
    
        spin_box.setRange(min_value, max_value)  # Set the allowed range of values
        spin_box.setValue(initial_value)
        spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spin_box.setFixedSize(QSize(30, 20))  # Set a fixed size
        spin_box.setStyleSheet("QSpinBox { font-size: " + str(self.font_size) + "pt; }")
        spin_box.setContentsMargins(0, 0, 0, 0)  # Remove margins for the QSpinBox

        font = spin_box.font()
        font.setPointSizeF(self.font_size)
        spin_box.setFont(font)

        # If a function was provided, connect the QSpinBox's editingFinished signal to it
        if function is not None:
            def on_editing_finished():
                function(spin_box)
            spin_box.editingFinished.connect(on_editing_finished)

        unit_label = QLabel(unit)
        unit_label.setStyleSheet("background-color: transparent;color: black;")  # Adjust color as needed
        unit_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = unit_label.font()
        font.setPointSizeF(self.font_size)
        unit_label.setFont(font)
        unit_label.setContentsMargins(1, 1, 0, 1)  # Set margins for the unit QLabel


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
        self.unit_labels.append((unit_label, unit, kwargs))  # Append the unit and kwargs for later language changes


    def update_spin_box(self, key, max_value):
        """
        Met à jour une boîte à filer avec la clé donnée.

        Args:
            key (str) : Clé de traduction pour la boîte à filer.
            max_value (int) : Nouvelle valeur maximale.
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
        Crée un bouton avec la clé donnée et l'ajoute au widget.

        Args:
            key (str) : Clé de traduction pour le bouton.
            function (fonction) : Fonction à appeler lors du clic sur le bouton.
            **kwargs : Arguments supplémentaires pour le constructeur QPushButton et pour la traduction.
        """
        button = QPushButton(self.translator.translate(key, **kwargs))
        if function is not None:
            button.clicked.connect(function)
        button_proxy = QGraphicsProxyWidget(self)
        button_proxy.setWidget(button)

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = button.font()
        font.setPointSizeF(self.font_size)
        button.setFont(font)

        button.setContentsMargins(1, 1, 1, 1)
        button.setStyleSheet("QPushButton { padding-top: 2px; }")
        self.layout.addItem(button_proxy)
        self.buttons.append((button, button_proxy, key, kwargs))  # Append the key for later language changes


    def update_button(self, key, state):
        """
        Met à jour un bouton avec la clé donnée.

        Args:
            key (str) : Clé de traduction pour le bouton.
            state (str) : Nouvel état à afficher sur le bouton
        """
        # Loop over all buttons
        for button, button_proxy, button_key, kwargs in self.buttons:
            # If the key matches
            if button_key == key:
                # Update the state in kwargs
                kwargs['state'] = state
                # Translate the new text and update the button
                button.setText(self.translator.translate(button_key, **kwargs))
                # We found the button, so we can break the loop
                break



    def create_label_with_indicator(self, key, color="black", **kwargs):
        """
        Met à jour un indicateur avec la clé et l'état donnés.

        Args:
            indicator : Indicateur à mettre à jour.
            key (str) : Clé de traduction pour l'indicateur.
            state (bool) : Nouvel état de l'indicateur.
        """
        # Create the label as before
        label_translate = {}
        for arg_name in ['alignment', 'indent', 'margin', 'text', 'wordWrap']: #argument du QLabel possible
            if arg_name in kwargs:
                label_translate[arg_name] = kwargs.pop(arg_name)

        label = QLabel(self.translator.translate(key, **kwargs), **label_translate)
        label.setStyleSheet(f"background-color: transparent;color: {color};")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setContentsMargins(0, 0, 0, 0)  # Set smaller margins for the unit QLabel

        font = label.font()
        font.setPointSizeF(self.font_size - 1)  # Reduce the font size
        label.setFont(font)

        # Create an indicator QLabel
        indicator = QLabel()
        indicator.setFixedSize(6, 6)  # Set a smaller fixed size for the indicator
        indicator.setStyleSheet("background-color: transparent;")  # Set transparent background

        # Create a QPixmap to draw the indicator
        pixmap = QPixmap(indicator.size())
        pixmap.fill(Qt.transparent)  # Fill with transparent color

        # Create a QPainter to draw on the QPixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing for a smoother circle

        # Set the color based on the state
        color = QColor("green")
        painter.setBrush(QBrush(color))

        # Draw the circle
        painter.drawEllipse(pixmap.rect())

        # End the QPainter
        painter.end()

        # Set the QPixmap as the indicator QLabel's pixmap
        indicator.setPixmap(pixmap)

        # Create a QHBoxLayout to hold the indicator and the label
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)  # Set smaller margins
        hbox.addWidget(indicator)
        hbox.addWidget(label)
        hbox.addStretch(1)  # Add a stretchable space

        # Create a QWidget to hold the QHBoxLayout
        widget = QWidget()
        widget.setLayout(hbox)
        widget.setStyleSheet("background-color: transparent;")  # Set transparent background

        # Create a QGraphicsProxyWidget to add the QWidget to the QGraphicsWidget
        widget_proxy = QGraphicsProxyWidget(self)
        widget_proxy.setWidget(widget)

        # Add the QGraphicsProxyWidget to the layout
        self.layout.addItem(widget_proxy)

        # Store the indicator QLabel for later updates
        self.labels.append((label, widget_proxy, key, kwargs))
        self.indicators.append((indicator, key, False))  # Add the indicator to the new list


    def update_indicator(self, indicator, key, state):
        """
        Met à jour un indicateur avec la clé et l'état donnés.

        Args:
            indicator : Indicateur à mettre à jour.
            key (str) : Clé de traduction lié à l'indicateur.
            state (bool) : Nouvel état de l'indicateur.
        """
        for indicator, indicator_key, _ in self.indicators:
            if indicator_key == key:
                pixmap = QPixmap(indicator.size())
                pixmap.fill(Qt.transparent)

                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                color = QColor("red") if state else QColor("green")
                painter.setBrush(QBrush(color))

                painter.drawEllipse(pixmap.rect())

                painter.end()

                indicator.setPixmap(pixmap)
                break

    def create_label_with_combo_box_and_button(self, key, combo_items=[], button_function=None, color="black", button_key="", **kwargs):
        """
        Crée une étiquette avec une boîte de combinaison et un bouton, et les ajoute au widget.

        Args:
            key (str) : Clé de traduction pour l'étiquette.
            combo_items (list) : Éléments à ajouter à la boîte de combinaison.
            button_function (fonction) : Fonction à appeler lors du clic sur le bouton.
            color (str) : Couleur du texte de l'étiquette.
            button_key (str) : Clé de traduction pour le bouton.
            **kwargs : Arguments supplémentaires pour les constructeurs QLabel, QComboBox, et QPushButton et pour la traduction.
        """
        label_translate = {}
        for arg_name in ['alignment', 'indent', 'margin', 'text', 'wordWrap']:  # argument du QLabel possible
            if arg_name in kwargs:
                label_translate[arg_name] = kwargs.pop(arg_name)

        label = QLabel(self.translator.translate(key, **kwargs), **label_translate)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setContentsMargins(1, 1, 0, 1)  # Set margins for the unit QLabel

        font = label.font()
        font.setPointSizeF(self.font_size)
        label.setFont(font)

        combo_box = QComboBox()
        combo_box.addItems(combo_items)
        combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        combo_box.setStyleSheet("QComboBox { font-size: " + str(self.font_size) + "pt; background-color: None; }")
        combo_box.setContentsMargins(0, 0, 0, 0)  # Remove margins for the QComboBox


        font = combo_box.font()
        font.setPointSizeF(self.font_size)
        combo_box.setFont(font)

        button = QPushButton(self.translator.translate(button_key, **kwargs))
        if button_function is not None:
            button.clicked.connect(button_function)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button.setStyleSheet("QPushButton { font-size: " + str(self.font_size) + "pt; background-color: None; }")
        button.setContentsMargins(1, 0, 0, 0)  # Remove margins for the QPushButton

        font = button.font()
        font.setPointSizeF(self.font_size)
        button.setFont(font)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)  # Set smaller margins
        hbox.addWidget(label)
        hbox.addWidget(combo_box)
        hbox.addWidget(button)
        hbox.addStretch(1)  # Add a stretchable space

        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")  # Set transparent background
        widget.setLayout(hbox)

        widget_proxy = QGraphicsProxyWidget(self)
        widget_proxy.setWidget(widget)

        self.layout.addItem(widget_proxy)

        self.labels.append((label, widget_proxy, key, kwargs))  # Append the key for later language changes
        self.combo_boxes.append((combo_box, key, kwargs))  # Append the initial value and kwargs for later language changes
        self.buttons.append((button, widget_proxy, button_key, kwargs))  # Append the key for later language changes
        widget_proxy.setZValue(1)


    def paint(self, painter, option, widget):
        """
        Dessine le widget.

        Args:
            painter (QPainter) : Objet de dessin utilisé pour peindre.
            option : Options de dessin.
            widget : Widget à dessiner.
        """
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 6, 6)
        painter.fillPath(path, QColor(self.color))


    def change_language(self):
        """
        Change la langue du widget pour toutes les éléments traduisibles.
        """
        for label, _ , key, kwargs in self.labels:
            label.setText(self.translator.translate(key,**kwargs))
        for button, _ , key, kwargs in self.buttons:
            button.setText(self.translator.translate(key,**kwargs))
        for unit_label, unit, kwargs in self.unit_labels:
            unit_label.setText(self.translator.translate(unit,**kwargs))  # Update the text of the unit QLabel

    def set_font_size(self,size):
        """
        Modifie la taille de la police du widget.

        Args:
            size (int) : Nouvelle taille de la police.
        """
        self.font_size = size


    def set_pos_size(self, width, height):
        """
        Définit la position et la taille du widget.

        Args:
            width (int) : Largeur du widget parent.
            height (int) : Hauteur du widget parent.
        """
        for label in self.labels:
            font = label[0].font()
            font.setPointSizeF(self.font_size)
            label[0].setFont(font)

        for button in self.buttons:
            font = button[0].font()
            font.setPointSizeF(self.font_size)
            button[0].setFont(font)
            #change button size
            button[0].setFixedWidth(int(width*self.ratio[0]))

        #number of élément in the layout
        nb_element = self.layout.count()
        for spin_box in self.spin_boxes:
            spin_box[0].setStyleSheet("QSpinBox { font-size: " + str(self.font_size-1) + "pt; }")
            spin_box[0].setFixedWidth(int(width*self.ratio[0]/3.5))  # Adjust the 4 as needed
            spin_box[0].setFixedHeight(int(height*self.ratio[1]/(nb_element*1.2)))

        for unit_label in self.unit_labels:
            font = unit_label[0].font()
            font.setPointSizeF(self.font_size)
            unit_label[0].setFont(font)
            
        for indicator, key, state in self.indicators:
            # Resize the indicator
            indicator.setFixedSize(8, 8)  # Convert to int
            # Update the indicator
            self.update_indicator(indicator, key, state)

        self.resize(width*self.ratio[0], height*self.ratio[1])
        self.maximumSize = self.size()
        self.setPos(width*self.position[0], height*self.position[1])
