from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QTableWidget,\
    QTableWidgetItem, QAbstractItemView, QComboBox, QTextEdit, QCheckBox, QScrollArea, QInputDialog
from managers.doc_manager import AV_material, Document


class AddDocument(QWidget):
    def __init__(self):
        super().__init__()
        doc_types = ("Book", "Journal", "AV")
        item, ok = QInputDialog.getItem(self, "Choose type", "", doc_types, 0, False)
        if ok and item:
            self.type = item
        else:
            self.type = None
            return
        self._set_up_ui()

    def _set_up_ui(self):
        window_size_x = 640
        window_size_y = 480

        document_name_label = QLabel("Name:")
        document_name_label.setFixedWidth(60)
        self.document_name = QLineEdit()

        document_author_label = QLabel("Author:")
        document_author_label.setFixedWidth(60)
        self.document_author = QLineEdit()

        #document_type_label = QLabel("type:")
        #document_type_label.setFixedWidth(60)
        #self.document_type = QComboBox()
        #document_genre_label = QLabel("genre:")
        #document_genre_label.setFixedWidth(60)
        #self.document_genre = QComboBox()

        document_cost_label = QLabel("Cost:")
        document_cost_label.setFixedWidth(60)
        self.document_cost = QLineEdit()
        cost_validator = QIntValidator()
        cost_validator.setBottom(0)
        self.document_cost.setValidator(cost_validator)

        document_description_label = QLabel("Description:")
        document_description_label.setFixedWidth(60)
        self.document_description = QTextEdit()

        #document_is_bestseller = QCheckBox()
        #document_is_bestseller.setText("Is bestseller")

        document_keywords_label = QLabel("Keywords:")
        self.document_keywords = QTextEdit()

        add_button = QPushButton("Add")
        add_button.setFixedWidth(90)
        add_button.setFixedHeight(25)
        add_button.clicked.connect(self.add_document)
#book section
        if self.type == "Book":
            document_edition_label = QLabel("Edition:")
            document_edition_label.setFixedWidth(60)
            self.document_edition = QLineEdit()

            document_publisher_label = QLabel("Publisher:")
            document_publisher_label.setFixedWidth(60)
            self.document_publisher = QLineEdit()

            document_year_label = QLabel("Year:")
            document_year_label.setFixedWidth(60)
            self.document_year = QLineEdit()
            cost_validator = QIntValidator(-10000, 2018)
            self.document_year.setValidator(cost_validator)
#end of book section
#journal section
        if self.type == "Journal":
            document_journal_label = QLabel("Journal:")
            document_journal_label.setFixedWidth(60)
            self.document_journal = QLineEdit()

            document_issue_label = QLabel("Issue:")
            document_issue_label.setFixedWidth(60)
            self.document_issue = QLineEdit()

            document_editor_label = QLabel("Editor:")
            document_editor_label.setFixedWidth(60)
            self.document_editor = QLineEdit()
#end of journal section

##################################################################

        vbox = QVBoxLayout()
        document_name_layout = QHBoxLayout()
        document_name_layout.addWidget(document_name_label)
        document_name_layout.addWidget(self.document_name)
        vbox.addLayout(document_name_layout)
        document_author_layout = QHBoxLayout()
        document_author_layout.addWidget(document_author_label)
        document_author_layout.addWidget(self.document_author)
        vbox.addLayout(document_author_layout)
        #document_type_layout = QHBoxLayout()
        #document_type_layout.addWidget(document_type_label)
        #document_type_layout.addWidget(self.document_type)
        #vbox.addLayout(document_type_layout)
        #document_genre_layout = QHBoxLayout()
        #document_genre_layout.addWidget(document_genre_label)
        #document_genre_layout.addWidget(self.document_genre)
        #vbox.addLayout(document_genre_layout)
        document_cost_layout = QHBoxLayout()
        document_cost_layout.addWidget(document_cost_label)
        document_cost_layout.addWidget(self.document_cost)
        vbox.addLayout(document_cost_layout)
#book section
        if self.type == "Book":
            document_edition_layout = QHBoxLayout()
            document_edition_layout.addWidget(document_edition_label)
            document_edition_layout.addWidget(self.document_edition)
            vbox.addLayout(document_edition_layout)
            document_publisher_layout = QHBoxLayout()
            document_publisher_layout.addWidget(document_publisher_label)
            document_publisher_layout.addWidget(self.document_publisher)
            vbox.addLayout(document_publisher_layout)
            document_year_layout = QHBoxLayout()
            document_year_layout.addWidget(document_year_label)
            document_year_layout.addWidget(self.document_year)
            vbox.addLayout(document_year_layout)
#end of book section
#journal section
        if self.type == "Journal":
            document_journal_layout = QHBoxLayout()
            document_journal_layout.addWidget(document_journal_label)
            document_journal_layout.addWidget(self.document_journal)
            vbox.addLayout(document_journal_layout)
            document_issue_layout = QHBoxLayout()
            document_issue_layout.addWidget(document_issue_label)
            document_issue_layout.addWidget(self.document_issue)
            vbox.addLayout(document_issue_layout)
            document_editor_layout = QHBoxLayout()
            document_editor_layout.addWidget(document_editor_label)
            document_editor_layout.addWidget(self.document_editor)
            vbox.addLayout(document_editor_layout)
#end of journal section
        #vbox.addWidget(document_is_bestseller)
        vbox.addWidget(document_description_label)
        vbox.addWidget(self.document_description)
        vbox.addWidget(document_keywords_label)
        vbox.addWidget(self.document_keywords)
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()
        add_button_layout.addWidget(add_button)
        vbox.addLayout(add_button_layout)

        self.setLayout(vbox)
        self.resize(window_size_x, window_size_y)
        self.setWindowTitle("Add " + self.type)

    def add_document(self):
        if self.type == "AV":
            AV_material.add({"title": self.document_name.text(), "author": self.document_author.text(), "cost": 123,
                         "keywords": self.document_keywords.toPlainText()})