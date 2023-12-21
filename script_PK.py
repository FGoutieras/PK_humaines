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
fetch_mmcif('2GU8', assembly=1) # on fetch la chaine correspondant à la PKACA humaine

nb_alpha_carbons=[]
rmsd_list=[]

for struct in list[0:10]:
    fetch_mmcif(struct, assembly=1)
    out = cmd.align(struct,"2GU8") #aligner la chaine qui correspond à la PKACA humaine, en récupérant le code sur la pdb
    string = "2GU8 and "+struct+" and name ca"
    cmd.select('alpha_carbons', "2GU8 and "+struct+" and name ca")
    nb_alpha_carbons.append(cmd.count('alpha_carbons'))
    rmsd, n_atoms, n_cycles, n_rmsd_pre, n_atom_pre, score, n_res = out
    rmsd_list.append(rmsd)
    
os.chdir("..")    
cmd.zoom()

# tout exporter dans un csv

rows = zip(list, nb_alpha_carbons, rmsd)

with open('data.csv', 'w', newline='') as f:
   writer = csv.writer(f)
   for row in rows:
       writer.writerow(row)