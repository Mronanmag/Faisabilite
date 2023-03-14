from librairie import *

class FormulaireClient(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.formulaire = QFormLayout()
        self.result = ""

        labelF = QLabel("Primer Forward")
        self.tb_primerF = QLineEdit()
        self.btnFindAmorceF = QPushButton("Amorce forward")

        labelR = QLabel("Primer Reverse")
        self.tb_primerR = QLineEdit()
        self.btnFindAmorceR = QPushButton("Amorce reverse ")

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
        self.formulaire.addRow(labelRegion, self.tb_genomique)

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
        self.send_file(ssh, file_fasta, "/home/ronan/Bioinfo/sequence.fasta")
        commande = "python3 Faisabilite.py -i sequence.fasta -f " + primer_forward + " -r " + primer_reverse + " -g " \
                   + region_genomique
        stdin, stdout, stderr = ssh.exec_command('cd Bioinfo && ' + commande)
        output = stdout.read().decode("utf-8")
        err = stderr.read().decode("utf-8")
        print(err)
        self.result = output
        # self.transfer_file(ssh)
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