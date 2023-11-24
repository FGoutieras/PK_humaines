import csv
from fetch_mmcif.py import fetch_mmcif

cmd.set('fetch_path', cmd.exp_path('./cif'), quiet=0)

def import_file(fichier,col):
    liste_struct=[]
    with open(fichier) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')    
        line_count = 0
        for row in csv_reader:
            if line_count<2:
                line_count+=1
            else:
                liste_struct.append(row[col])
    return(liste_struct)

list = import_file("O15530_pdb.csv",1)

cmd.fetch_mmcif("2GU8",assembly=1)

for struct in list[0:5]:
    cmd.fetch_mmcif(struct, assembly=1)
    cmd.align(struct,"2GU8")
cmd.zoom()