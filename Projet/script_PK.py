import csv 
import os

cmd.run('fetch_mmcif.py')

def extractPDB_IDs(infile):
    """
    Parse CSV file to extract the PDB IDs
    """
    ID_list = []
    with open(infile, 'r') as file:
        csvfile = csv.reader(file)
        for i in range(2):
            next(csvfile) # skip the header rows
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

    # Load the protein structures of extracted proteins from CSV
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

def alignment(PDB_IDs, ref="2GU8", refined=False):
    """
    Aligns all the structures in the list to the reference and prints an error message if te RMSD is too high (> 4)
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
# Uncomment the next line if pymol crashes when trying to align all the proteins from the list
# list = list[0:10] 
loadStructures(list)
splitStates(list)
list = cmd.get_object_list()
alignment(list)
alignment(list, refined=True)
getAlphaCarbons(list)