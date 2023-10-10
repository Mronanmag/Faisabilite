import sys


from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QFormLayout,
    QWidget,
    QHBoxLayout,
)

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        self.setWindowTitle("Etude de faisabilité")
        self.setCentralWidget(FormWidget())

class FormWidget(QWidget) :
    def __init__(self) :
        super().__init__()
        self.widget()
        self.style()
        self.layout()

    def style(self) :
        self.setStyleSheet('''
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #0077cc;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0055aa;
            }
            QPushButton:pressed {
                background-color: #003388;
            }
        ''')



    def widget(self) :
        self.lb_forward = QLabel("Primer Forward (5' -3')")
        self.le_forward = QLineEdit()
        self.lb_reverse = QLabel("Primer Reverse (5' - 3')")
        self.le_reverse = QLineEdit()
        self.lb_overlap_f = QLabel("Overlap forward")
        self.le_overlap_f = QLineEdit()
        self.lb_overlap_r =  QLabel("Overlap reverse")
        self.le_overlap_r = QLineEdit()
        self.lb_fasta = QLabel("Fichier fasta")
        self.le_fasta = QLineEdit()
        self.btn_send = QPushButton("Lancer l'analyse")
        self.btn_primer_forward = QPushButton("Forward primer")
        self.btn_primer_reverse = QPushButton("Reverse primer")
        self.btn_find_fasta = QPushButton("Chercher")
        self.btn_find_primer = QPushButton("Couple primer")
        self.widget_button = QWidget()


    def layout(self) :
        self.button_layout = QHBoxLayout()
        self.form = QFormLayout()
        self.form.addRow(self.lb_forward,self.le_forward)
        self.form.addRow(self.lb_reverse,self.le_reverse)
        self.form.addRow(self.lb_overlap_f,self.le_overlap_f)
        self.form.addRow(self.lb_overlap_r,self.le_overlap_r)
        self.form.addRow(self.lb_fasta,self.le_fasta)
        self.button_layout.addWidget(self.btn_find_primer) 
        self.button_layout.addWidget(self.btn_primer_forward)
        self.button_layout.addWidget(self.btn_primer_reverse)
        self.button_layout.addWidget(self.btn_find_fasta)
        self.button_layout.addWidget(self.btn_send)
        self.widget_button.setLayout(self.button_layout)
        self.form.addWidget(self.widget_button)
        self.setLayout(self.form)

    def connect(self) :
        pass

    



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
