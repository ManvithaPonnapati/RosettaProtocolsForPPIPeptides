
This repo is a list of Rosetta scripts that have been compiled using help from Rosetta tutorials, discussion threads and documentation. Given a complex of two interacting proteins, it allows design of peptide fragments that contribute the most to the binding energy 

To design a peptide binder that can bind to protein X, we start with the PDB structure of Protein X in complex with Y. For this example we are using the PDB structure 6M0J which is a complex between ACE2 and SARS-CoV-2 spike protein. We will design a peptide fragment that can bind to SARS-CoV-2 spike protein and is derived from ACE2.

The following steps use the protocols - PeptiDerive, FlexPepDock, RosettaDock and FlexDDG. 


Step 1: Clean the PDB File using Notebook 1. This removes anything other ATOM* lines from your PDB file. 

Step 2: Split chain A and chain E from the 6m0j into separate pdb files

Step 3: Relax chain A and chain E pdb files using the fast relax script above. You can read more about the options used here - https://new.rosettacommons.org/docs/latest/application_documentation/structure_prediction/relax

Step 4: Using PyMOL and the original clean PDB of 6m0j align the relaxed chains A and E to their respective counterparts in the original PDB of 6m0j. And save the aligned and relaxed chains to a new PDB. We will use this PDB throughout the next steps. 

Step 5: To obtain the fragments of peptides between 10-150 that contribute the most to the binding energy, we will run the peptiderive script at each length. Utilize peptiderive.py and peptiderive.sh as described in the PeptiDerive folder. The output is a results.csv file which contains the sequence and the binding energy contribution of the linear fragment. To read more about peptiderive - https://new.rosettacommons.org/docs/latest/application_documentation/analysis/PeptiDerive

Step 6: We will dock the peptide fragments against the old spike protein and the new spike protein using RosettaDock and FlexPepDock. The scripts and the README for running these protocols is under - DockingMethods. 

Step 7: Score the models from the docking methods using InterfaceAnalyzer script under Analysis folder. 

Step 8: After experimental validation, Step 9 and Step 10 will run computational mutagenesis. 

Step 9: We will run the computational mutagenesis using the backrub xml scripts provided by FlexDDG protocol. To run the mutagenesis across the whole protein, use the scripts in Mutagenesis - you need to provide a path to your pdb, and an output path. FlexDDG creates a db3 file as an output

Step 10: Use the analyze.py in the Mutagenesis folder to obtain a plot of all mutations and their corresponding ddG value 

There is no guarantee that the output of this protocol will correlate one-to-one with experimental results. We also noticed sensitivity to the parameters used for different Rosetta protocols. Parameters were chosen using the respective protocol documentation. Please note that FlexDDG takes a long amount of time to run. We are grateful to MIT Media Lab's internal matlabers and MIT supercloud for providing us with the computing resources

UPDATE: This github also contains the data used in the paper - https://www.nature.com/articles/s42003-020-01470-7 . Please note that there is an update to the plots in Fig 3 mutagenesis plots. The new plots were generated with an updated protocol and analysis scripts. The new plots shows that the computational pipeline correctly predicts the mutations that didn’t work in the experimental screens. 
