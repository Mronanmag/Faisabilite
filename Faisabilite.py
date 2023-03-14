import getopt
import os
import subprocess
import sys
import re
from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo.Consensus import *
from Bio.Phylo.Consensus import bootstrap


from matplotlib import pyplot as plt


class FastaPrimaire() :

    def __init__(self) :
        self.species = []
        self.region = ""
        self.amorce_forward = ""
        self.amorce_reverse = ""
        self.len_forward = 0
        self.len_reverse = 0
        self.path_fasta = ""
        self.correspondaceGI = {}

    def setSpecies(self,species):
        print(species)
        try :
            fi = open(str(species),"r")
            ligne = fi.readline()
            while ligne != "" :
                self.species.append(ligne.strip())
                ligne = fi.readline()
        except :
            print("Le fichier species est introuvable")
            sys.exit(2)

    def setRegion(self,region):
        self.region = region.strip()

    def setAmorceForward(self,forward):
        self.amorce_forward = forward.replace("I","N").replace("U","T")
        self.len_forward = int((len(self.amorce_forward) * 2) / 3)

    def setAmorceReverse(self,reverse) :
        self.amorce_reverse = reverse.replace("I","N").replace("U","T")
        self.len_reverse = int((len(self.amorce_reverse) * 2) / 3)


    def setPathFasta(self,path):
        self.path_fasta = str(path)


    def removeForwardPrimer(self):
        self.nom_fichier_f = "Output/" + str(self.region + "_f.fasta")
        nom_fichier_log = "Output/" + self.region + "_f.log"
        fo = open(self.nom_fichier_f,"w")
        fe = open(nom_fichier_log,"w")
        subprocess.run(["cutadapt", self.path_fasta,"-g " + self.amorce_forward, "-O "+ str(self.len_forward),
                        "--discard-untrimmed"], stdout = fo, stderr = fe)
        fo.close()
        fe.close()

    def removeReversePrimer(self):
        self.nom_fichier_r = "Output/" + self.region + "_f_r.fasta"
        nom_fichier_log = "Output/" + self.region + "_f_r.log"
        fo = open(self.nom_fichier_r,"w")
        fe = open(nom_fichier_log,"w")
        subprocess.run(["cutadapt",self.nom_fichier_f ,"-a " + self.amorce_reverse , "-O "+ str(self.len_reverse),
                        "--discard-untrimmed","-M","2000"], stdout = fo, stderr= fe)
        fo.close()
        fe.close()

    def alignementClustal(self):
        if self.nom_fichier_r :
            self.nom_alignement = "Output/" + self.region + "_algn.aln"
            fo = open(self.nom_alignement,"w")
            fe = open("Output/" + self.region+"_algn.log","w")
            subprocess.run(["clustalo","-i" , self.nom_fichier_r, "--outfmt","clustal","--threads","16"],stdout = fo, stderr= fe)
        else :
            print("Vous devez d'abords trimmer vos adaptateur")

    def alignementMafft(self):
        if self.nom_fichier_r :
            self.nom_alignement = "Output/" + self.region + "_algn.mafft"
            fo = open(self.nom_alignement,"w")
            fe = open("Output/" + self.region+"_algn.log","w")
            subprocess.run(["mafft","--maxiterate","1000","--localpair", "--thread","16", self.nom_fichier_r],stdout = fo, stderr= fe)

    def arbrePhylo(self):
        if self.nom_alignement :
            align = AlignIO.read(self.nom_alignement, "clustal")
            calculator = DistanceCalculator("blosum62")
            constructor = DistanceTreeConstructor(calculator)
            tree = constructor.build_tree(align)
            Phylo.draw_ascii(tree)

    def arbreIqtree2(self):
        if self.nom_alignement :
            subprocess.run(["iqtree2", "-s", self.nom_alignement,"-nt", "16"])
            #Build tree
            arbre = Phylo.read("Output/" + self.region + "_algn.mafft.treefile", "newick")
            Phylo.draw_ascii(arbre)
            #Draw tree
            Phylo.draw(arbre, do_show=False)
            plt.savefig("Output/" + self.region + "_algn.mafft.png")
            plt.close()


    def recupererArgument(self):
        argv = sys.argv[1:]
        try :
            opts, args = getopt.getopt(argv,"h:i:f:r:g:s:",["--input_file","--forward_primer","--reverse_primer",
                                                         "--region","--species"])
        except getopt.GetoptError:
            print("python Faisabilite.py -i(input_file) -f(forward_primer) -r(reverse_primer) -g(region) -s(species)")
            sys.exit(2)
        for opt,arg in opts :
            if opt == "-h" :
                print("python Faisabilite.py -i(input_file) -f(forward_primer) -r(reverse_primer) -g(region) -s(species)")
                sys.exit(2)
            elif opt in("-i","--input_file") :
                self.setPathFasta(arg)
            elif opt in("-f","--forward_primer") :
                self.setAmorceForward(arg)
            elif opt in("-r","--reverse_primer") :
                self.setAmorceReverse(arg)
            elif opt in("-g","--region") :
                self.setRegion(arg)
            elif opt in("-s","--species") :
                self.setSpecies(arg)

    def statistiqueFichierFasta(self,fasta) :
        print("Début statistique")
        fi = open(fasta,"r")
        ligne = fi.readline()
        fasta_glo = {}
        motif=r'^(>\w+\.\d) (\w+ \w+)'
        while ligne != "" :
            if ">" in ligne :
                try :
                    nom_sequence = ">" + re.search(motif,ligne).group(2).replace(" ","_") + "_" + re.search(motif,ligne).group(1).replace(" ","_").replace(">","") 
                    fasta_glo[nom_sequence] = ""
                except : 
                    nom_sequence = ligne.strip()
                    fasta_glo[nom_sequence] = ""
            else :
                fasta_glo[nom_sequence] += ligne.strip()
            ligne = fi.readline()
        taille_fichier = len(fasta_glo)
        longueur_moyenne = self.calculTailleMoyFasta(fasta_glo)
        fo = open("Output/" + self.region + "_f_r_formated.fasta","w")
        for k,v in sorted(fasta_glo.items(), key=lambda x:x[0]) :
            fo.write(k+"\n"+v+"\n")
        fo.close()
        self.nom_fichier_r = "Output/" + self.region + "_f_r_formated.fasta"
        print("Nombre de séquence : ", taille_fichier)
        print("La longueur moyenne des séquences est : ",longueur_moyenne)
        print("Fin statistique")
    
    def calculTailleMoyFasta(self,fasta) :
        tot = 0
        for k,v in fasta.items() :
            tot += len(v)
        if tot != 0 :
            return tot / len(fasta)
        else : 
            print("Il n'y a pas de séquence dans le fichier fasta final")
            sys.exit(2) 
    

    def checkVariable(self):

        print(self.species)
        print(self.region)
        print(self.amorce_forward)
        print(self.amorce_reverse)
        print(self.len_forward)
        print(self.len_reverse)
        print(self.path_fasta)

    def ecrirePrimer(self) :
        fo = open("Output/" + self.region+"_primer.txt","w")
        fo.write("5\'"+self.amorce_forward+"\'3'"+"\n")
        fo.write("3\'"+self.amorce_reverse+"\'5'"+"\n")
        fo.close()



def verifierLogiciel():
    try :
        print("Version de clustalo : ", os.popen("clustalo --version").read().strip())
        print("Version de cutadapt : ", os.popen("cutadapt --version").read().strip())
        print("Version de phyml : ", os.popen("phyml-mpi --version").read().strip())
    except :
        print("Vous devez installer clustalo, cutadapt et phyml")

verifierLogiciel()
f = FastaPrimaire()
f.recupererArgument()
print("1 - Supression des primers forward")
f.removeForwardPrimer()
print("1 - Fin Supression des primers forward")
print("2 - Supression des primer reverse")
f.removeReversePrimer()
print("2 - Fin Supression des primer reverse")
print("3 - Alignement des séquuences clustal")
f.statistiqueFichierFasta(f.nom_fichier_r)
f.alignementMafft()
print("3 -  Fin Alignement des séquuences clustal")
print("4 -  Génération de l'arbre phylogénique")
f.arbreIqtree2()
print("4 -  Fin Génération de l'arbre phylogénique")
f.ecrirePrimer()
