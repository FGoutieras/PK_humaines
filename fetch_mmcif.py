# Copyright 2022-2023 Stefano Trapani stefano.trapani@umontpellier.fr
#
# 2023-10-04   uses connect_mode=4
# 2023-10-01   uses atom ID now (rather that atom index)
#              sets numeric_type=0 for all unobserved residues
#              (these have been excluded from processing in order to avoid a
#              bug in PyMOL 2.5, which incorrectly handles unobserved residues
#              with insertion codes)
# 2023-09-13   updated file download urls
# 2022-10-09   created by Stefano Trapani

from pymol import cmd
import            pymol

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fetch_mmcif(code, name=None, assembly=0, path=".", file=None, quiet=0):
    """
DESCRIPTION

    "fetch_mmcif" downloads a PDBx/mmcif file (asymmetric unit or biological 
    assembly) from https://files.wwpdb.org or read it from disk:

    - if a file named <code>-assembly<assembly>.cif.gz (or <code>.cif.gz if 
      assembly==0) already exists in <path>, then the existing file will be 
      read;
    - otherwise, the file will be retrieved from the internet and saved in 
      <path>.

    This command redefines the numeric_type property by storing in it the 
    residue sequential numbers (from PDBx/mmcif label_seq_id fields).  

USAGE

    fetch_mmcif code [, name [, assembly [, path [, file]]]]

ARGUMENTS

    code = a single PDB identifier.

    name = the object name into which the file should be loaded (default: 
           <code>-assembly<assembly> or <code> if assembly==0).

    assembly = the biological assembly id (default 0 = asymmetric unit)

NOTES

    this command redefines the numeric_type property by storing in it the 
    residue sequential numbers (from PDBx/mmcif label_seq_id fields).

    mmcif files are loaded using connect_mode=4

PYMOL API

    fetch_mmcif(string code, string name, int assembly, string path, string file, int quiet)

    """
    CODE=code
    ASSEMBLY=int(assembly)
    print(ASSEMBLY)
    NAME=name
    if NAME is None:
        NAME=CODE
        if ASSEMBLY>0:
            NAME+="-assembly"+str(ASSEMBLY)
    PATH=path
    FILE=file
    if FILE is None:
        FILE=CODE
        if ASSEMBLY>0:
            FILE+="-assembly"+str(ASSEMBLY)
        FILE+=".cif.gz"
    QUIET=int(quiet)
    
    # keep track of initial values of host_Paths_cif and connect_mode
    host_Paths_cif_0=pymol.importing.hostPaths["cif"]
    connect_mode_0=cmd.get('connect_mode')
    #
    cmd.set('connect_mode',4)
    #
    if ASSEMBLY==0 :
        pymol.importing.hostPaths["cif"] = "https://files.wwpdb.org/download/{code}.cif.gz"
    elif ASSEMBLY>0 :
        pymol.importing.hostPaths["cif"] = "https://files.wwpdb.org/download/{code}-assembly"+str(ASSEMBLY)+".cif.gz"
    if not QUIET:
        print(' Using import path: ',pymol.importing.hostPaths["cif"])
    
    # temporary fetch : retrieve the sequential residue numbers (label_seq_id)
    #my_space={'label_seq_id':[0]}                                                         # 2022-10-01_OLD
    my_space={'label_seq_id':{}}                                                           # 2022-10-01_NEW
    cif_use_auth_0=cmd.get('cif_use_auth')
    cmd.set('cif_use_auth',0)
    cmd.fetch(CODE, NAME, async_=0, path=PATH, file=FILE, quiet=QUIET)
    if not QUIET:
        print(" Retrieving sequential residue numbers (label_seq_id) ...")
    sel=cmd.get_unused_name()                                                              # 2022-10-01_NEW
    cmd.select(sel,NAME,state=1) # exclude unobserved residues to avoid incorrect handling # 2022-10-01_NEW
                                 # of residues with insertion codes (PyMOL 2.5 bug)        # 2022-10-01_NEW
    #cmd.iterate(NAME,'label_seq_id.append(resv)',space=my_space,quiet=QUIET)              # 2022-10-01_OLD
    cmd.iterate(sel,'label_seq_id[ID]=resv',space=my_space,quiet=QUIET)                    # 2022-10-01_NEW
    cmd.delete(NAME)
    cmd.delete(sel)                                                                        # 2022-10-01_NEW
    cmd.set('cif_use_auth',cif_use_auth_0)
    #
    # final fetch: store sequential residue numer (label_seq_id) as numeric_type
    cmd.fetch(CODE, NAME, async_=0, path=PATH, file=FILE, quiet=1)
    #cmd.alter(NAME,'numeric_type=label_seq_id[index]',space=my_space,quiet=QUIET)         # 2022-10-01_OLD
    Nat=0                                                                                  # 2022-10-01_NEW
    for ID,seq_id in my_space['label_seq_id'].items():                                     # 2022-10-01_NEW
        Nat+=1                                                                             # 2022-10-01_NEW
        cmd.alter(f'{NAME} and id {ID}',f'numeric_type={seq_id}',space=my_space,quiet=1)   # 2022-10-01_NEW
    if not QUIET:
        #print(" Sequential residue numbers (label_seq_id) stored as numeric_type")                 # 2022-10-01_OLD
        print(f" Sequential residue numbers (label_seq_id) stored as numeric_type for {Nat} atoms") # 2022-10-01_NEW
    del my_space
    #
    # reset initial value of host_Paths_cif and connect_mode
    pymol.importing.hostPaths["cif"] = host_Paths_cif_0
    cmd.set('connect_mode',connect_mode_0)
    
    return
cmd.extend('fetch_mmcif',fetch_mmcif)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
