import csv 
import os

cmd.run('fetch_mmcif.py')

def extractPDB_IDs(infile):
    """
    Extrait les ID PDB du fichier PDB et les met dans une liste
    """
    ID_list = []
    with open(infile, 'r') as file:
        csvfile = csv.reader(file)
        for i in range(2):
            next(csvfile) # ignore les 2 premières lignes (en-tête)
        for row in csvfile:
            ID_list.append(row[1])
    return ID_list

def loadStructures(PDB_IDs, ref="2GU8"):
    """
    Charge la référence et toutes les structures de la liste dans le dossie SUPER
    """
    os.chdir("../Super")
    # Structure choisie de la PKACA humaine (code UniProt P17612)
    fetch_mmcif(code=ref, name=ref, assembly=1)

    # Charge les structures du CSV
    for code in PDB_IDs:
        fetch_mmcif(code=code, name=code, assembly=1)
        cmd.remove("all and not polym")
    os.chdir("../Projet")  

def splitStates(PDB_IDs):
    """
    Sépare les states de l'objet moléculaire en plusieurs objets distincts si existant
    """
    for object in PDB_IDs:
        stateCount = cmd.count_states(object)
        if stateCount > 1:
            cmd.split_states(object)
            cmd.delete(object)

def getAlphaCarbons(object, ref="2GU8"):
    """
    Affiche et retourne une liste du nombre de C-alpha par objet
    """
    return cmd.count_atoms(ref + " and " + object + " and name ca")

def alignment(PDB_IDs, ref="2GU8", refined=False):
    """
    Aligne toutes les structures dans la liste par rapport à la référence
    et affiche un message d'erreur si le RMSD est est trop haut (> 4)
    """
    table = ["PDB_ID","chaîne", "Nb_C_alpha", "RMSD"]
    cLobe = " and resi 183-207" # DFG-APE de 2GU8
    for code in PDB_IDs:
        if code != ref:
            if refined==False:
                rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = cmd.align(mobile=code, target=ref, quiet=1)
            else:
                rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = cmd.align(mobile=code + cLobe, target=ref + cLobe, quiet=1)
                table.append([code, 
                              cmd.get_chains(code),
                              getAlphaCarbons(code),
                              rmsd
                             ])
            if rmsd > 4:
                print("Problème lors de l'alignement de la structure ",code,", protéine non prise en compte (RMSD =",rmsd,")", sep="")
    cmd.zoom()
    return table

# MAIN
file = "rcsb_pdb_custom_report.csv"
list = extractPDB_IDs(file)
list = list[0:10] # on garde que les 10 premiers objets pour tester plus facilement
loadStructures(list)
splitStates(list)
list = cmd.get_object_list()
alignment(list)
alignment(list, refined=True)
getAlphaCarbons(list)
