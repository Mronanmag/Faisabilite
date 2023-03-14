from librairie import *

class PoPupAmorcesForward(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.orientation = ""
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('/home/bioinfo/BDD/ProjetAmorcesV1.db')
        self.db.open()

        self.combo_box = QComboBox()
        self.update_combo_box()

        self.button = QPushButton("Valider")
        self.button.clicked.connect(self.handle_button)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def update_combo_box(self):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT nom_amorce FROM amorces WHERE orientation=\"forward\"")
        self.combo_box.clear()
        while query.next():
            self.combo_box.addItem(query.value(0))

    def handle_button(self):
        selected_item = self.combo_box.currentText()
        query = QtSql.QSqlQuery()
        query.exec_("SELECT sequence FROM amorces WHERE nom_amorce=\""+selected_item+"\"")
        query.next()
        self.amorce = query.value(0)
        self.accept()

class PoPupAmorcesReverse(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.orientation = ""
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('/home/bioinfo/BDD/ProjetAmorcesV1.db')
        self.db.open()

        self.combo_box = QComboBox()
        self.update_combo_box()

        self.button = QPushButton("Valider")
        self.button.clicked.connect(self.handle_button)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def update_combo_box(self):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT nom_amorce FROM amorces WHERE orientation=\"reverse\"")
        self.combo_box.clear()
        while query.next():
            self.combo_box.addItem(query.value(0))

    def handle_button(self):
        selected_item = self.combo_box.currentText()
        query = QtSql.QSqlQuery()
        query.exec_("SELECT sequence FROM amorces WHERE nom_amorce=\""+selected_item+"\"")
        query.next()
        self.amorce = query.value(0)
        self.accept()
