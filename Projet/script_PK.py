import csv 
import os

cmd.run('fetch_mmcif.py')

# Extracts the PDB IDs from the given .csv file and puts them into a list
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

# load the reference and all the structures from the given list in the Super folder
def loadStructures(PDB_IDs, ref="2GU8"):
    """
    Load the protein structures: reference and extracted ones
    """
    os.chdir("../Super")
    # Structure choisie de la PKACA humaine (code UniProt P17612)
    fetch_mmcif(code=ref, name=ref, assembly=1)

    # Load the protein structures of extracted proteins from CSV
    for code in PDB_IDs:
        fetch_mmcif(code=code, name=code, assembly=1)
        cmd.remove("all and not polym")
    os.chdir("../Projet")  

# je saurais pas l'expliquer 
def splitStates(PDB_IDs):
    for object in PDB_IDs:
        stateCount = cmd.count_states(object)
        if stateCount > 1:
            cmd.split_states(object)
            cmd.delete(object)

# aligns all the structures in the list to the reference and prints an error message if te RMSD is too high (> 4)
def simpleAlignment(PDB_IDs, ref="2GU8"):
    for code in PDB_IDs:
        if code != ref:
            rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = cmd.align(mobile=code, target=ref, quiet=1)
            if rmsd > 4:
                print("Problème lors de l'alignement de la structure ",code,", RMSD =",rmsd, sep="")
    cmd.zoom()

# prints and returns a list of the number of alpha carbons in each alignment
def getAlphaCarbons(list, ref="2GU8"):
    for struct in list:
        name = struct + "_alpha_carbons"
        cmd.select(name, ref + " and "+struct+" and name ca")
        nb_alpha_carbons.append(cmd.count_atoms(name))
    print(nb_alpha_carbons)
    return(nb_alpha_carbons)

nb_alpha_carbons=[]
rmsd_list=[]

file = "rcsb_pdb_custom_report.csv"
list = extractPDB_IDs(file)
list = list[0:10]
loadStructures(list)
splitStates(list)
list = cmd.get_object_list()
simpleAlignment(list)
getAlphaCarbons(list)
