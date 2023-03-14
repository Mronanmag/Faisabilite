import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QComboBox, QWidget, QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import paramiko

class Formulaire(QWidget):
    def __init__(self):
        super().__init__()
        self.formulaire = QFormLayout()
        self.result = ""

        labelF = QLabel("Primer Forward")
        self.tb_primerF = QLineEdit()
        labelR = QLabel("Primer Reverse")
        self.tb_primerR = QLineEdit()
        self.formulaire.addRow(labelF, self.tb_primerF)
        self.formulaire.addRow(labelR, self.tb_primerR)

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
        primer_forward, primer_reverse, reverse_complement, file_fasta, region_genomique = self.get_info()
        ssh = self.connect_ssh()
        if not ssh:
            return
        self.send_file(ssh,file_fasta,"/home/ronan/Bioinfo/sequence.fasta")
        commande = "python3 Faisabilite.py -i sequence.fasta -f " + primer_forward + " -r " + primer_reverse + " -g " \
         + region_genomique
        stdin, stdout, stderr = ssh.exec_command('cd Bioinfo && '+ commande)
        output = stdout.read().decode("utf-8")
        print(output)
        self.result = output
        #self.transfer_file(ssh)
        ssh.close()

    def connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect('192.168.1.64', username='ronan', password='root')
            print("connexion ok")
            return ssh
        except Exception as e:
            print("Erreur lors de la connexion SSH:", e)
            return None

    def transfer_file(self, ssh, file_input, file_return):
        sftp = ssh.open_sftp()
        sftp.get(file_input, file_return)
        sftp.close()

    def send_file(self, ssh, file_path, remote_path):
        sftp = ssh.open_sftp()
        sftp.put(file_path, remote_path)
        sftp.close()


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
        font = QFont()
        font.setPointSize(20)
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
        self.display_text.setText(self.form.result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PrimerMain()
    main.show()
    sys.exit(app.exec_())

