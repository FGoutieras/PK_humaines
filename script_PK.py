import csv

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

list = import_file("test.csv",1)

cmd.fetch("2GU8")

for struct in list:
    cmd.fetch(struct)
    cmd.align(struct,"2GU8")