from Resolution import FastaFindSpecies
from Resolution import Request
from Resolution import FileCharge
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

		#Ouvertur du formulaire pour récupérer les séquences du couple choisi dans la BDD
		self.open_form_action = QAction("Ouvrir formulaire", self)
		self.open_form_action.triggered.connect(self.showFormC)
		self.form.btnFindCouple.clicked.connect(self.showFormC)



		#Creation d'une zone de texte avec possibilité de scroll vertical et horizontal  et non modifiable et prêt a recevoir du texte ascii avec une chasse fixe
		self.display_text = QTextEdit()
		self.display_text.setReadOnly(True)
		self.display_text.setAcceptRichText(False)
		self.display_text.setLineWrapMode(QTextEdit.NoWrap)
		self.display_text.setFontFamily("monospace")

		self.resolution_widget = ResolutionWidget()
		

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
		main_layout.addWidget(top_bar, 0,0,1,1)
		main_layout.addWidget(self.form, 1, 0,1,1)
		#La taille du display text doit être agrandie et correspondre à 2/3 de la fenetre
		main_layout.addWidget(self.display_text, 1, 1,4,4)
		main_layout.addWidget(self.resolution_widget,2,0,1,1)

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

	def showFormC(self):
		dialog = PoPupCouples(self)
		dialog.exec_()
		self.form.tb_primerF.setText(dialog.amorceF)
		self.form.tb_primerR.setText(dialog.amorceR)
		self.form.tb_genomique.setText(dialog.nameCouple)

	def cleanDisplayText(self):
		self.display_text.clear()

class ResolutionWidget(QWidget) :
	def __init__(self,parent=None):
		super().__init__(parent)
		self.chargeFile()
		self.widget()
		self.layout()

	def chargeFile(self):
		self.names = FileCharge()
		self.nodes = FileCharge()
		self.names.ChargerNames()
		self.nodes.ChargerNodes()

	def widget(self):
		self.lb_choice = QLabel("Quel est le rang taxonomique recherché")
		self.le_choice = QLineEdit()
		self.lb_fasta = QLabel("Fichier fasta généré : ")
		self.le_fasta = QLineEdit()
		self.btn_fasta = QPushButton("Find")
		self.lb_resolution = QLabel("Taux de résolution")
		self.le_resolution = QLineEdit()
		self.btn_calculate = QPushButton('Calculate')

	def layout(self):
		self.main_layout = QVBoxLayout()
		self.layout_querie = QHBoxLayout()
		self.layout_querie.addWidget(self.lb_choice)
		self.layout_querie.addWidget(self.le_choice)
		self.layout_fichier = QHBoxLayout()
		self.layout_fichier.addWidget(self.lb_fasta)
		self.layout_fichier.addWidget(self.le_fasta)
		self.layout_fichier.addWidget(self.btn_fasta)
		self.layout_resolution = QHBoxLayout()
		self.layout_resolution.addWidget(self.lb_resolution)
		self.layout_resolution.addWidget(self.le_resolution)
		self.layout_resolution.addWidget(self.btn_calculate)
		self.main_layout.addLayout(self.layout_querie)	
		self.main_layout.addLayout(self.layout_fichier)
		self.main_layout.addLayout(self.layout_resolution)
		self.setLayout(self.main_layout)


	def getChoice(self) :
		if isinstance(self.le_choice.text(), str) :
			return self.le_choice.text()
		return False

	def getFile(self) :
		return self.le_fasta.text()	

	def connect(self) :
		pass

	def calculate(self) :
		rq = Request(self.name.fichier,self.nodes.fichier)
		querie = self.getChoice()		
		if querie :
			rq.setQuerie(querie)
			rq.setSpeciesList()			
			ffs = FastaFindSpecies(self.getFile())
			ffs.compare2list(rq.species_list_therique,ffs.liste_species_fasta)
			

    # def browse_file(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.ReadOnly
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "All Files (*);;Python Files (*.py)",
    #                                                options=options)
    #     if file_name:
    #         pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = PrimerMain()
	main.show()
	sys.exit(app.exec_())

