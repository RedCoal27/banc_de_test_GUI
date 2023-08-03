from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListView, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem



class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.translator = parent.translator
        self.setWindowTitle(self.translator.translate("Help"))
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.list_view = QListView()
        self.model = QStandardItemModel(self.list_view)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Set a fixed width for the list widget
        self.list_view.setFixedWidth(100)

        # Add categories to the list widget
        self.add_category("Category 1")
        self.add_category("Category 2")
        # Add more categories as needed

        self.list_view.setModel(self.model)
        self.list_view.selectionModel().currentChanged.connect(self.display_help)

        # Set stylesheets for the widgets
        self.list_view.setStyleSheet("""
            background-color: #f0f0f0;
            border: none;
        """)
        self.text_edit.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #dddddd;
            padding: 1px;
        """)

        layout.addWidget(self.list_view)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def add_category(self, category):
        item = QStandardItem(self.translator.translate(category))
        item.setData(self.translator.translate(f"Documentation for {category} goes here..."), Qt.UserRole + 1)
        item.setTextAlignment(Qt.AlignCenter)  # Center the text
        self.model.appendRow(item)

    def display_help(self, current, previous):
        if current:
            self.text_edit.setPlainText(current.data(Qt.UserRole + 1))
            self.text_edit.setAlignment(Qt.AlignCenter)
