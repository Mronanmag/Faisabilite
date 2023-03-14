import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QComboBox, QWidget, QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import paramiko
import subprocess

class Formulaire(QWidget):
    def __init__(self):
        super().__init__()
        self.formulaire = QFormLayout()
        self.result = ""

        labelF = QLabel("Primer Forward")
        self.tb_primerF = QLineEdit()
        self.btnFindAmorceF = QPushButton("Amorce forward")
        

        labelR = QLabel("Primer Reverse")
        self.tb_primerR = QLineEdit()
        self.btnFindAmorceR = QPushButton("Amorce reverse ")

        self.btnFindAmorceF.clicked.connect(self.openPopUp)

        self.layoutForward = QHBoxLayout()
        self.layoutReverse = QHBoxLayout()

        self.layoutForward.addWidget(self.tb_primerF)
        self.layoutForward.addWidget(self.btnFindAmorceF)

        self.layoutReverse.addWidget(self.tb_primerR)
        self.layoutReverse.addWidget(self.btnFindAmorceR)

        self.formulaire.addRow(labelF, self.layoutForward)
        self.formulaire.addRow(labelR, self.layoutReverse)

        label_reversecomplement = QLabel("Reverse complément")
        self.cb_rc = QCheckBox()
        self.formulaire.addRow(label_reversecomplement, self.cb_rc)

        labelRegion = QLabel("Region génomique")
        self.tb_genomique = QLineEdit()
        self.formulaire.addRow(labelRegion,self.tb_genomique)

        label_fichieFasta = QLabel("Fichier fasta")
        self.line_edit = QLineEdit()
        self.browse_button = QPushButton("Parcourir")
        self.browse_button.clicked.connect(self.browse_file)
        self.layoutRechercheFichier = QHBoxLayout()
        self.layoutRechercheFichier.addWidget(self.line_edit)
        self.layoutRechercheFichier.addWidget(self.browse_button)
        self.formulaire.addRow(label_fichieFasta, self.layoutRechercheFichier)

        self.btn_sendRequest = QPushButton("Envoyer")
        self.btn_sendRequest.clicked.connect(self.sendRequest)
        self.formulaire.addWidget(self.btn_sendRequest)
        self.setLayout(self.formulaire)

    def openPopUp(self) :
        pop = PoPupAmorces()
        pop.setWindowModality(Qt.ApplicationModal)
        pop.show()

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "All Files (*);;Python Files (*.py)",
                                                   options=options)
        if file_name:
            self.line_edit.setText(file_name)

    def get_info(self):
        primer_forward = self.tb_primerF.text()
        primer_reverse = self.tb_primerR.text()
        reverse_complement = self.cb_rc.isChecked()
        file_fasta = self.line_edit.text()
        region_genomique = self.tb_genomique.text()
        return (primer_forward, primer_reverse, reverse_complement, file_fasta, region_genomique)

    def sendRequest(self):
        print("test")
        primer_forward, primer_reverse, reverse_complement, file_fasta, region_genomique = self.get_info()
        commande = "python3 Faisabilite.py -i sequence.fasta -f " + primer_forward + " -r " + primer_reverse + " -g " \
         + region_genomique
        fe = open("faisabilite.log","a")
        fo = open("result.txt","w")
        subprocess.run(["python3","Faisabilite.py","-i",file_fasta,"-f",primer_forward,"-r",primer_reverse,"-g",region_genomique],stdout=fo, stderr= fe)
        fe.close()
        fo.close()

class PoPupAmorces(QWidget) :
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.setWindowTitle("Choix amorces")
        self.btn = QPushButton()
        self.btn.clicked.connect(self.test_amorces)
        pos = QGridLayout()
        pos.addWidget(self.btn)
        self.setLayout(pos)

    def test_amorces(self) :
        self.close()

class PrimerMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form = Formulaire()
        self.form.btn_sendRequest.clicked.connect(self.update_main_windows)
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)  # set margins to 0 on all sides
        top_bar_layout.setAlignment(Qt.AlignHCenter)  # align the layout to the center
        top_bar.setLayout(top_bar_layout)

        # create a QLabel for the text
        title_label = QLabel("Vérifier les amorces sur un fichier fasta")

        # set the font for the label
        font = QFont("monospace",12)
        font.setPointSize(12)
        font.setBold(True)
        title_label.setFont(font)

        # add the label to the layout
        top_bar_layout.addWidget(title_label)

        main_layout = QGridLayout()
        main_layout.addWidget(top_bar, 0, 0, 1, 2)
        main_layout.addWidget(self.form, 1, 0)
        main_layout.addWidget(self.display_text, 1, 1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle('Primer check')
        self.Width = 1080
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

    def update_main_windows(self):
        self.display_text.clear()
        fo = open("result.txt")
        ligne = fo.readline()
        affichage = ""
        while ligne != "" :
            affichage += ligne
            ligne = fo.readline()
        self.display_text.setText(affichage)
        print("Done")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PrimerMain()
    main.show()
    sys.exit(app.exec_())

