from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListView, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        """
        Constructeur de la classe HelpDialog.

        Args:
            parent: Objet parent.
        """
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.translator = parent.translator
        self.setWindowTitle(self.translator.translate("Help"))
        self.resize(800, 400)
        self.init_ui()

    def init_ui(self):
        """
        Initialise l'interface utilisateur de la fenêtre d'aide.
        """
        layout = QHBoxLayout()
        self.list_view = QListView()
        self.model = QStandardItemModel(self.list_view)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Set a fixed width for the list widget
        self.list_view.setFixedWidth(300)

        # Add categories to the list widget
        categories = {
            "manuel_automatic": "manuel_automatic_description",
            "interlock": "interlock_description",
            "roughing_pump": "roughing_pump_description",
            "turbo_pump": "turbo_pump_description",
            "iso_nupro": "iso_nupro_description",
            "gate_turbo": "gate_turbo_description",
            "wafer_lift_slit_valve": "wafer_lift_slit_valve_description",
            "mfc": "mfc_description",
            "baratron": "baratron_description",
            "jauge_pirani": "jauge_pirani_description",
            "throttle_valve": "not_defined",
            "motor_lift": "not_defined",
            "convectron": "not_defined",
        }

        self.add_categories(categories)

        self.list_view.setModel(self.model)
        self.list_view.selectionModel().currentChanged.connect(self.display_help)

        # Set stylesheets for the widgets
        self.list_view.setStyleSheet("""
            background-color: #f0f0f0;
            border: none;
        """)
        self.text_edit.setStyleSheet("""
            background-color: #fdfdfd;
            border: 1px solid #dddddd;
            padding: 1px;
        """)

        layout.addWidget(self.list_view)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def add_categories(self, categories):
        """
        Ajoute les catégories à la liste de catégories.

        Args:
            categories: Dictionnaire de catégories et de clés de contenu associées.
        """
        for category_key, content_key in categories.items():
            item = QStandardItem(self.translator.translate(category_key))
            item.setData(self.translator.translate(content_key), Qt.UserRole + 1)
            item.setTextAlignment(Qt.AlignJustify)  # Center the text
            item.setEditable(False)
            self.model.appendRow(item)

    def display_help(self, current, previous):
        """
        Affiche le contenu d'aide correspondant à la catégorie sélectionnée.

        Args:
            current: Élément de la liste actuellement sélectionné.
            previous: Élément précédemment sélectionné. (inutilisé mais requis par le signal)
        """
        if current:
            self.text_edit.setPlainText(current.data(Qt.UserRole + 1))
            self.text_edit.setAlignment(Qt.AlignJustify)
