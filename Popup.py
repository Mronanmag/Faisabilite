from librairie import *

class PoPupAmorcesForward(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.orientation = ""
		try :
			self.db = mariadb.connect(
					user = "pc_bioinfo",
					password="eE8*a-Ww.W",
					host="10.4.5.251",
					port=3306,
					database="NGS_Db")
		except mariadb.Error as e:
			print("Erreur de connexion à la base des amorces ngs :",e)
 
		self.combo_box = QComboBox()
		self.update_combo_box()

		self.button = QPushButton("Valider")
		self.button.clicked.connect(self.handle_button)

		layout = QVBoxLayout()
		layout.addWidget(self.combo_box)
		layout.addWidget(self.button)
		self.setLayout(layout)

	def update_combo_box(self): 
		self.cur = self.db.cursor()
		self.cur.execute("SELECT nom_amorce FROM amorces WHERE orientation =\"forward\"")
		result = self.cur.fetchall()
		for row in result :
			self.combo_box.addItem(str(row[0]))

	def handle_button(self):
		selected_item = self.combo_box.currentText()
		self.cur.execute("SELECT sequence FROM amorces WHERE nom_amorce=\""+selected_item+"\"")
		self.amorce = self.cur.fetchone()[0]
		self.accept()



class PoPupAmorcesReverse(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.orientation = ""
		try :
			self.db = mariadb.connect(
					user = "pc_bioinfo",
					password="eE8*a-Ww.W",
					host="10.4.5.251",
					port=3306,
					database="NGS_Db")
		except mariadb.Error as e:
			print("Erreur de connexion à la base des amorces ngs :",e)
 
		self.combo_box = QComboBox()
		self.update_combo_box()

		self.button = QPushButton("Valider")
		self.button.clicked.connect(self.handle_button)

		layout = QVBoxLayout()
		layout.addWidget(self.combo_box)
		layout.addWidget(self.button)
		self.setLayout(layout)

	def update_combo_box(self): 
		self.cur = self.db.cursor()
		self.cur.execute("SELECT nom_amorce FROM amorces WHERE orientation =\"reverse\"")
		result = self.cur.fetchall()
		for row in result :
			self.combo_box.addItem(str(row[0]))

	def handle_button(self):
		selected_item = self.combo_box.currentText()
		self.cur.execute("SELECT sequence FROM amorces WHERE nom_amorce=\""+selected_item+"\"")
		self.amorce = self.cur.fetchone()[0]
		self.accept()

class PoPupCouples(QDialog) :
	def __init__(self,parent=None) :
		super().__init__(parent)
		try :
			self.db = mariadb.connect(
					user = "pc_bioinfo",
					password="eE8*a-Ww.W",
					host="10.4.5.251",
					port=3306,
					database="NGS_Db")
		except mariadb.Error as e:
			print("Erreur de connexion à la base des amorces ngs :",e)
		
		self.combo_box = QComboBox()
		self.update_combo_box()

		self.button = QPushButton("Valider")
		self.button.clicked.connect(self.handle_button)

		layout = QVBoxLayout()
		layout.addWidget(self.combo_box)
		layout.addWidget(self.button)
		self.setLayout(layout)

	def update_combo_box(self): 
		self.cur = self.db.cursor()
		self.cur.execute("SELECT `nom_couple` FROM `couple`")
		result = self.cur.fetchall()
		for row in result :
			self.combo_box.addItem(str(row[0]))

	def handle_button(self):
		selected_item = self.combo_box.currentText()
		print(selected_item)
		self.cur.execute("SELECT a1.sequence, a2.sequence FROM couple INNER JOIN amorces a1, amorces a2 WHERE couple.amorce_couple_1 = a1.id_amorce AND couple.amorce_couple_2 = a2.id_amorce AND nom_couple = \""+selected_item+"\"")
		amorces = self.cur.fetchall()
		self.amorceF = amorces[0][0]
		self.amorceR = amorces[0][1]
		self.accept()

