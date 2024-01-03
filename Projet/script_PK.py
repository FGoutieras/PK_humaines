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
    Load the protein structures: reference and extracted ones
    """
    os.chdir("./Super")
    # Structure choisie de la PKACA humaine (code UniProt P17612)
    fetch_mmcif(code=ref, name=ref, assembly=1)

    # Load the protein structures of extracted proteins from CSV
    for code in PDB_IDs:
        fetch_mmcif(code=code, name=code, assembly=1)
        cmd.remove("all and not polym")
    os.chdir("..")  

def splitStates(PDB_IDs):
    for object in PDB_IDs:
        stateCount = cmd.count_states(object)
        if stateCount > 1:
            cmd.split_states(object)
            cmd.delete(object)

def simpleAlignment(PDB_IDs, ref="2GU8"):
    for code in PDB_IDs:
        if code != ref:
            rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = cmd.align(mobile=code, target=ref, quiet=0)
            if rmsd > 4:
                print("Problème lors de l'alignement de la structure",code)

def getAlphaCarbons(list, ref="2GU8"):
    for struct in list:
        name = struct + "_alpha_carbons"
        cmd.select(name, ref + " and "+struct+" and name ca")
        nb_alpha_carbons.append(cmd.count_atoms(name))
    print(nb_alpha_carbons)
    return(nb_alpha_carbons)
        

nb_alpha_carbons=[]
rmsd_list=[]

infile = "rcsb_pdb_custom_report.csv"
list = extractPDB_IDs(infile)
list = list[0:2]
loadStructures(list)
splitStates(list)
list = cmd.get_object_list()
simpleAlignment(list)
getAlphaCarbons(list)

cmd.zoom()

# rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = out
# rmsd_list.append(rmsd)
