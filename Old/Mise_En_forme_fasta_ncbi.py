import re

def statistiqueFichierFasta(fasta):
    fi = open(fasta, "r")
    ligne = fi.readline()
    fasta_glo = {}
    motif = r'^(>\w+\.\d) (\w+ \w+)'
    while ligne != "":
        if ">" in ligne:
            try:
                nom_sequence = ">" + re.search(motif, ligne).group(2).replace(" ", "_") + "_" + re.search(motif,ligne).group(1).replace(" ", "_").replace(">", "")
                fasta_glo[nom_sequence] = ""
            except:
                nom_sequence = ligne.strip()
                fasta_glo[nom_sequence] = ""
        else:
            fasta_glo[nom_sequence] += ligne.strip()
        ligne = fi.readline()
    fo = open("/home/bioinfo/Téléchargements/fasta_formated.fasta", "w")
    print(fasta_glo)
    for k, v in sorted(fasta_glo.items(), key=lambda x: x[0]):
        if "Laminaria_digitata" in k or "Laminaria_hyperborea" in k :
            fo.write(k + "\n" + v + "\n")
    fo.close()


fi = "/home/bioinfo/Téléchargements/sequence.fasta"
statistiqueFichierFasta(fi)
