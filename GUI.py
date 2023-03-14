from librairie import *

class PrimerMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form = FormulaireServeur()

        #Association pour mettre à jour display_text
        self.form.btn_sendRequest.clicked.connect(self.update_main_windows)
        self.form.btnDelete.clicked.connect(self.cleanDisplayText)
        self.form.btnSave.clicked.connect(self.cleanDisplayText)
        #Ouverture du formulaire pour révupérer les amorces de la bases sqlite
        self.open_form_action = QAction("Ouvrir formulaire",self)
        self.open_form_action.triggered.connect(self.showFormF)
        self.form.btnFindAmorceF.clicked.connect(self.showFormF)

        #Ouverture du formulaire pour révupérer les amorces de la bases sqlite
        self.open_form_action = QAction("Ouvrir formulaire",self)
        self.open_form_action.triggered.connect(self.showFormR)
        self.form.btnFindAmorceR.clicked.connect(self.showFormR)



        #Creation d'une zone de texte avec possibilité de scroll vertical et horizontal  et non modifiable et prêt a recevoir du texte ascii avec une chasse fixe
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setAcceptRichText(False)
        self.display_text.setLineWrapMode(QTextEdit.NoWrap)
        self.display_text.setFontFamily("monospace")


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
        #La taille du display text doit être agrandie et correspondre à 2/3 de la fenetre
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
        if os.path.exists("result.txt"):
            tab = []
            fo = open("result.txt", "r")
            ligne = fo.readline()
            while ligne != "":
                tab.append(ligne)
                ligne = fo.readline()
            self.display_text.append("".join(tab))
        else :
            self.display_text.append("Aucun fichier résultat n'a été chargé")

    def showFormF(self):
        dialog = PoPupAmorcesForward(self)
        dialog.exec_()
        self.form.tb_primerF.setText(dialog.amorce)

    def showFormR(self):
        dialog = PoPupAmorcesReverse(self)
        dialog.exec_()
        self.form.tb_primerR.setText(dialog.amorce)

    def cleanDisplayText(self):
        self.display_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PrimerMain()
    main.show()
    sys.exit(app.exec_())

