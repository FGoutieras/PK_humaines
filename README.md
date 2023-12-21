# PK_humaines
Devoir - Structures des PK humaines

## A tester:
- Un tableau montrant les résultats de la superposition des structures (sur lesquelles vous aurez travaillé) sur la PKACA ciblée.
    PDB ID  | N° unité biologique utilisée | Chaîne utilisée pour la superposition | Nb. C-alpha superposés | RMSD (Å)

## A faire:
- Pour la superposition :
    i) optimiser la superposition des C-lobes
    ii) vous devez utiliser les fichiers contenant les assemblages biologiques (et non l'unité asymétrique) des structures (répéter plusieurs fois la superposition si plusieurs assemblages biologiques sont proposés dans la PDB) ;
    iii) utiliser comme repère (dans le cas de complexes oligomériques) juste la (ou une des) chaîne(s) de la PK d'intérêt présente(s) dans le complexe.
    - un dossier appelé "Super/" contenant les structures des PK que vous aurez superposées à la PKACA + le fichier de la PKACA ciblé (tous au format mmcif).
- Une figure (en ribbon) montrant les unités biologiques superposées.
- Mettre en évidence les cas où la superposition n'aurait pas abouti et en expliquer la raison.

## Fait:
- Établir une liste de structures PDB contenant la protéine-kinase assignée à votre groupe
Écrire une procédure (code python pour PyMOL) pour charger et superposer chacune de ces structures à une structure (de votre choix) de la PKACA humaine (code UniProt P17612).