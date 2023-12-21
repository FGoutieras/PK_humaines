import csv
import os

cmd.run('fetch_mmcif.py')
# cmd.set('fetch_path', cmd.exp_path('./cif'), quiet=0)

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

os.chdir("./cif")
fetch_mmcif('2GU8', name='2GU8', assembly=1) # on fetch la chaine correspondant à la PKACA humaine
time.sleep(1) # wait for 1 second

for struct in list[0:2]:
    fetch_mmcif(struct, name=struct, assembly=1)
    time.sleep(1) # wait for 1 second
    cmd.align(struct,"2GU8") #aligner la chaine qui correspond à la PKACA humaine, en récupérant le code sur la pdb
os.chdir("..")    
cmd.zoom()