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
    Load the protein structures in the Super folder: reference and extracted ones
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
    Splits the states of the molecular object into several distincts objects
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

def getAlphaCarbons(list, ref="2GU8"):
    """
    Prints and returns a list of the number of alpha carbons for each alignment 
    """
    for struct in list:
        if struct in cmd.get_object_list():
            name = struct + "_alpha_carbons"
            cmd.select(name, ref + " and "+struct+" and name ca")
            nb_alpha_carbons.append(cmd.count_atoms(name))
    print(nb_alpha_carbons)
    return(nb_alpha_carbons)

nb_alpha_carbons=[]
rmsd_list=[]

file = "rcsb_pdb_custom_report.csv"
list = extractPDB_IDs(file)
# Uncomment to fix crashes
# list = list[0:10]
loadStructures(list)
splitStates(list)
list = cmd.get_object_list()
alignment(list)
alignment(list, refined=True)
getAlphaCarbons(list)