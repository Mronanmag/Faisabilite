from librairie import *
from revcom import rev_function

class FormulaireServeur(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.formulaire = QFormLayout()
        self.result = ""

        labelF = QLabel("Primer Forward")
        self.tb_primerF = QLineEdit()
        self.btnFindAmorceF = QPushButton("Forward primer")

        labelOverlapF = QLabel("Overlap Forward")
        self.tb_overlapF = QLineEdit()

        labelOverlapR = QLabel("Overlap Reverse")
        self.tb_overlapR = QLineEdit()


        labelR = QLabel("Primer Reverse")
        self.tb_primerR = QLineEdit()
        self.btnFindAmorceR = QPushButton("Reverse primer ")

        self.btnFindCouple = QPushButton("Pair primer")
        self.formulaire.addRow(self.btnFindCouple)

        self.layoutForward = QHBoxLayout()
        self.layoutReverse = QHBoxLayout()

        self.layoutForward.addWidget(self.tb_primerF)
        self.layoutForward.addWidget(self.btnFindAmorceF)

        self.layoutReverse.addWidget(self.tb_primerR)
        self.layoutReverse.addWidget(self.btnFindAmorceR)

        self.formulaire.addRow(labelF, self.layoutForward)
        self.formulaire.addRow(labelOverlapF, self.tb_overlapF)
        self.formulaire.addRow(labelR, self.layoutReverse)
        self.formulaire.addRow(labelOverlapR, self.tb_overlapR)

        label_reversecomplement = QLabel("Reverse complément")
        self.cb_rc = QCheckBox()
        self.formulaire.addRow(label_reversecomplement, self.cb_rc)
        self.cb_rc.clicked.connect(self.revCompSeq)

        labelRegion = QLabel("Region génomique")
        self.tb_genomique = QLineEdit()
        self.formulaire.addRow(labelRegion, self.tb_genomique)

        label_fichieFasta = QLabel("Fichier fasta")
        self.line_edit = QLineEdit()
        self.browse_button = QPushButton("Find")
        self.browse_button.clicked.connect(self.browse_file)
        self.layoutRechercheFichier = QHBoxLayout()
        self.layoutRechercheFichier.addWidget(self.line_edit)
        self.layoutRechercheFichier.addWidget(self.browse_button)
        self.formulaire.addRow(label_fichieFasta, self.layoutRechercheFichier)

        # Création des boutons save ou delete pour conserver ou non les fichiers sortant du programme
        self.btnSave = QPushButton("Save")
        self.btnDelete = QPushButton("Delete")
        self.btn_sendRequest = QPushButton("Send request")

        self.layoutBtn = QVBoxLayout()
        self.layoutBtn.addWidget(self.btnDelete)
        self.layoutBtn.addWidget(self.btnSave)
        self.layoutBtn.addWidget(self.btn_sendRequest)

        #Pas nécessaire si aucune analyse donc sont caché par défaut
        self.btnDelete.hide()
        self.btnSave.hide()

        self.btn_sendRequest.clicked.connect(self.sendRequest)
        self.btnDelete.clicked.connect(self.deleteFile)
        self.btnSave.clicked.connect(self.saveFile)
        self.formulaire.addRow(self.layoutBtn)
        self.setLayout(self.formulaire)


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
        overlapF = self.tb_overlapF.text()
        overlapR = self.tb_overlapR.text()
        return (primer_forward, primer_reverse, reverse_complement, file_fasta, region_genomique,overlapF,overlapR)

    def sendRequest(self):
        print("Analyse en cours")
        self.btn_sendRequest.hide()
        self.btnDelete.show()
        self.btnSave.show()
        primer_forward, primer_reverse, reverse_complement, file_fasta, region_genomique,overlapF,overlapR = self.get_info()
        fe = open("faisabilite.log","w")
        fo = open("result.txt","w")
        subprocess.run(["python3","Faisabilite.py","-i",file_fasta,"-f",primer_forward,"-r",primer_reverse,"-g",region_genomique,"-m",overlapF,"-n",overlapR],stdout=fo, stderr= fe)
        fe.close()
        fo.close()
        print("Analyse terminée")

    def saveFile(self):
        print("Save file")
        #Ouvre une fenetre pour choisir un repertoire
        directory = QFileDialog.getExistingDirectory(self, "Select Directory") + "/"
        output_repertoire = directory + self.tb_genomique.text() + "/"
        repertoire_existe = self.checkExist(output_repertoire)
        if repertoire_existe == False:
            os.mkdir(output_repertoire)
            shutil.move("result.txt", output_repertoire)
            shutil.move("faisabilite.log", output_repertoire)
            files = os.listdir("Output/")
            for file in files:
                shutil.move("Output/" + file, output_repertoire)
            self.btnDelete.hide()
            self.btnSave.hide()
            self.btn_sendRequest.show()
            self.tb_primerF.clear()
            self.tb_primerR.clear()
            self.tb_genomique.clear()
            self.PopUpSave()
        else :
            self.PopUpNotSave()
            print("Le repertoire existe déjà")

    def revCompSeq(self) :
        self.tb_primerR.setText(rev_function(self.tb_primerR.text()))


    def deleteFile(self):
        print("Delete file")
        self.btnDelete.hide()
        self.btnSave.hide()
        self.btn_sendRequest.show()
        self.tb_genomique.clear()
        self.tb_overlapF.clear()
        self.tb_overlapR.clear()
        os.remove("result.txt")
        os.remove("faisabilite.log")
        files = os.listdir("Output/")
        for file in files:
            os.remove("Output/" + file)
        self.PopUpDelete()

    def checkExist(self, output_repertoire) :
        return os.path.exists(output_repertoire)

    def PopUpNotSave(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Le fichier existe déja dans le répertoire\nVeuillez choisir un autre répertoire")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def PopUpSave(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Le fichier a bien été sauvegardé")
        msg.setWindowTitle("Save")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def PopUpDelete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Les fichiers ont bien été supprimés")
        msg.setWindowTitle("Delete")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
