from Bio.PDB import *
import nglview as nv
import os
direcs = ['/Users/manvithaponnapati/Documents/Spring2020/CoronaVirus/102/']
pdb_results = []
for direc in direcs:
    for files in os.listdir(direc):
        pdb_info = {}
        if files.endswith("pdb"):
            
            pdb_info = {"peptide_name":files}
            with open(os.path.join(direc,files),"r") as f:
                lines = f.readlines()
                print(len("scored_mins_2ajfmin2ajf-receptorE_partnerA_"))
                if("scored_mins_2ajfmin2ajf-receptorE_partnerA_" in files):
                    file_number = files[43:46].replace("a","")
                pdb_info["pep_length"] =file_number
                for line in lines:
                    if len(line.split()) > 0:
                        split_line = line.split()
                        
                        if(split_line[0]=="pose"):
                            pdb_info["total_score"] = split_line[-1]
                        if (split_line[0] == "reweighted_sc"):
                            pdb_info["reweighted_sc"] = split_line[1]
                        if (split_line[0] == "pep_sc_noref"):
                            pdb_info["pep_sc_noref"] = split_line[1]
                        if (split_line[0] == "pep_sc"):
                            pdb_info["pep_sc"] = split_line[1]
                        if (split_line[0] == "I_bsa"):
                            pdb_info["I_bsa"] = split_line[1]
                        if (split_line[0] == "I_hb"):
                            pdb_info["I_hb"] = split_line[1]
                        if (split_line[0] == "I_pack"):
                            pdb_info["I_pack"] = split_line[1]
                        if (split_line[0] == "I_sc"):
                            pdb_info["I_sc"] = split_line[1]
                        if (split_line[0] == "I_unsat"):
                            pdb_info["I_unsat"] = split_line[1]

            pdb_results.append(pdb_info)