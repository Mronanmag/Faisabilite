import threading



class FileCharge():

    def __init__(self):
        self.fichier = ""

    def setFichier(self, fichier):
        self.fichier = fichier

    def ChargerNames(self):
        with open("/home/bioinfo/Application/OneDrive/Pipeline_to_frogs/names.dmp","r") as fopen : 
            print("INITIALISATION CHARGEMENT FICHIER names.dmp")
            liste = []
            dictionnaire_names = {}
            ligne = fopen.readline()
            while ligne != "":
                ligne = ligne.replace("\n", "")
                ligne = ligne.split("|")
                ligne = [elem.replace("\t", "") for elem in ligne]
                if ligne[1] not in dictionnaire_names.keys() :
                    dictionnaire_names[ligne[1].replace("_"," ")] = [ligne[0],ligne[3]]
                else :
                    if ligne[3] == "scientific name" :
                        dictionnaire_names[ligne[2].replace("_"," ")] = [ligne[0],ligne[3]]
                ligne = fopen.readline()
            self.setFichier(dictionnaire_names)
            print("FIN CHARGEMENT FICHIER names.dmp")
        fopen.close()


    def ChargerNodes(self):
        with open("/home/bioinfo/Application/OneDrive/Pipeline_to_frogs/nodes.dmp","r") as fopen :
            print("INITIALISATION CHARGEMENT FICHIER nodes.dmp")
            liste = []
            ligne = fopen.readline()
            dict_nodes = {}
            while ligne != "":
                ligne = ligne.replace("\n", "")
                ligne = ligne.split("|")
                ligne = [elem.replace("\t", "") for elem in ligne]
                dict_nodes[ligne[0]] = [ligne[1],ligne[2]]
                liste.append(ligne)
                ligne = fopen.readline()
            self.setFichier(dict_nodes)
            print("FIN CHARGEMENT FICHIER nodes.dmp")

class Request() :
    def __init__(self,names_dict,nodes_dict) :
        super().__init__()
        self.names = names_dict
        self.nodes = nodes_dict
        self.rank = ""
        self.querie = ""
        self.list_result = []

    def setRank(self,rank) :
        self.rank = rank

    def setQuerie(self,querie) :
        self.querie = querie

    def findAllSpecies(self) :
        num_querie = self.names.get(self.querie,'Not found')
        if num_querie[1] != "scientific name" or num_querie == 'Not found' :
            return "L'élément recherché n'est pas un nom scientifique veuillez reesayer avec le nom scientifique adapté"
        print(num_querie)
        liste_species = self.getKeysNodes(self.nodes,num_querie[0])
        for species in liste_species :
            print(species)
            name = self.getKeysScientificName(self.names,species)
            print(name)
            rank = self.names[name[0]]
            print(rank)

    


    def getKeys(self,dictionnaire,value) :
        keys = []
        for key in dictionnaire.items() :
            if key[1][0] == value : 
                keys.append(key[0])
        return keys

    def getKeysScientificName(self,dictionnaire,value) :
        keys = []
        for key in dictionnaire.items() :
            if key[1][0] == value and key[1][1] == "scientific name" :
                keys.append(key)
        return keys

    def getKeysNodes(self,dictionnaire,value) :
        keys = []
        for key,v in dictionnaire.items() :
            if v[0] == value :
                keys.append(key)
        return keys

names = FileCharge()
names.ChargerNames()
nodes = FileCharge()
nodes.ChargerNodes()
rq = Request(names.fichier,nodes.fichier)
rq.setQuerie("Ulva")
rq.findAllSpecies()









# def liste_ulva() :
#     name = filecharge()
#     nodes = filecharge()
#
#     # create threads for the functions
#     t1 = threading.thread(target=name.chargernames)
#     t2 = threading.thread(target=nodes.chargernodes)
#
#     # start the threads
#     t1.start()
#     t2.start()
#
#     # wait for the threads to finish
#     t1.join()
#     t2.join()
#
#     with open("extract_ulva_names.txt", "r") as f : 
#         species = []
#         lignes = f.readlines()
#         for ligne in lignes : 
#             ligne = ligne.strip().replace("\t","").split("|")
#             rank = nodes.fichier.get(ligne[0])[1]
#             if ligne[3] == 'scientific name' :
#                 if rank == 'species' :
#                    species.append(ligne[1]) 
#     species.sort()
#     for specie in species : 
#         print(specie)
#
# def liste_primer_primer(file) :
#     species = []
#     with open(file,"r") as f :
#         lignes = f.readlines()
#         for ligne in lignes : 
#             if ligne.startswith('>') :
#                 especes = ligne.replace(">","").split("_")
#                 especes = " ".join(especes[:2])
#                 species.append(especes)
#     return species
#
# # euk18s = liste_primer_primer("/media/bioinfo/Data/Faisabilite/Ulva/SHF1R4/SHF1R4_f_r_formated.fasta")
# # euk18s = list(set(euk18s))
# # euk18s.sort()
# # for s in euk18s :
# #     print(s)
# #
#
#
# def final() :
#     with open("liste_species_ulva.txt","r") as f :
#         liste_ulva = f.readlines()
#     with open("liste_species_ulva_v4.txt","r") as f : 
#         list_v4 = f.readlines()
#     with open("liste_species_ulva_ssu.txt","r") as f : 
#         liste_ssu = f.readlines()
#     with open("liste_species_ulva_tufA.txt") as f :
#         liste_tufA = f.readlines()
#     with open("liste_species_ulva_euk18s.txt") as f :
#         liste_euk = f.readlines()
#     with open(r"liste_species_ulva_SHF1R4.txt") as f :
#         liste_rbcl = f.readlines()
#
#
#
#     dict_final = {}
#     for species in liste_ulva :
#         dict_final[species] = []
#         if species in list_v4 :
#             dict_final[species].append(1)
#         else : 
#             dict_final[species].append(0)
#         if species in liste_ssu :
#             dict_final[species].append(1)
#         else : 
#             dict_final[species].append(0)
#         if species in liste_tufA :
#             dict_final[species].append(1)
#         else : 
#             dict_final[species].append(0)
#         if species in liste_euk :
#             dict_final[species].append(1)
#         else :
#             dict_final[species].append(0)
#         if species in liste_rbcl :
#             dict_final[species].append(1)
#         else :
#             dict_final[species].append(0)
#
#     for k,v in dict_final.items() : 
#         print(f"{k.strip()}\t{v[0]}\t{v[1]}\t{v[2]}\t{v[3]}\t{v[4]}")
#
#
# final()
