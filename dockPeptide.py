from pymol import stored
import math
from glob import glob
import os

pathPrefix="/home/perry/covid/StraPep"

# get receptor chain centroid coordinates
xyz = cmd.get_coords("6m0j and chain E", 1)
centroidR = [0, 0, 0]
for c in xyz:
    for i in range(3):
        centroidR[i] += c[i]
for i in range(3):
    centroidR[i] /= len(xyz)

# get peptide centroid coordinates
xyz = cmd.get_coords("6m0j and chain A", 1)
centroidP = [0, 0, 0]
for c in xyz:
    for i in range(3):
        centroidP[i] += c[i]
for i in range(3):
    centroidP[i] /= len(xyz)

# calculate translation vector
vector = [0, 0, 0]
for i in range(3):
    vector[i] = centroidP[i] - centroidR[i]

# normalize translation vector
mag  = 0
for i in range(3):
    mag += vector[i] ** 2
mag = math.sqrt(mag)
for i in range(3):
    vector[i] /= mag

print(vector)

# Based on https://pymolwiki.org/index.php/InterfaceResidues
# distCutoff = the cutoff to consider a residue as interacting
# residCutoff = how many residues are ok to be intracting
def dockPeptide(peptide, receptor = '6m0j', receptorChain = 'E', peptideChain='A', selName='interface', distCutoff=1, residCutoff=20):
    cmd.load("%s/data/%s.pdb" % (pathPrefix, peptide))
    cmd.align(peptide, "%s and chain %s" % (receptor, peptideChain))

    # Save user's settings, before setting dot_solvent
    oldDS = cmd.get("dot_solvent")
    cmd.set("dot_solvent", 1)

    while True:
        # iterate as long as there are intersecting residues

        # set some string names for temporary objects/selections
        tempC, selName1 = "tempComplex", selName+"1"
        chP, chR = "chP", "chR"

        # operate on a new object & turn off the original
        cmd.create(tempC, "%s or (%s and chain %s)" % (peptide, receptor, receptorChain))
        cmd.disable(peptide)
        cmd.disable(receptor)

        # get the area of the complete complex
        cmd.get_area(tempC, load_b=1)
        # copy the areas from the loaded b to the q, field.
        cmd.alter(tempC, 'q=b')
        #
        # extract the two chains and calc. the new area
        # note: the q fields are copied to the new objects
        # chA and chB
        cmd.extract(chP, tempC + " and (chain A)")
        cmd.extract(chR, tempC + " and (chain E)")
        cmd.get_area(chP, load_b=1)
        cmd.get_area(chR, load_b=1)
        #
        # # update the chain-only objects w/the difference
        cmd.alter( "%s or %s" % (chP,chR), "b=b-q" )

        # The calculations are done.  Now, all we need to
        # do is to determine which residues are over the cutoff
        # and save them.
        stored.r, rVal, seen = [], [], []
        cmd.iterate('%s or %s' % (chP, chR), 'stored.r.append((model,resi,b))')

        cmd.enable(peptide)
        cmd.enable(receptor)
        cmd.select(selName1, None)
        for (model,resi,diff) in stored.r:
            key=resi+"-"+model
            if abs(diff)>=float(distCutoff):
                if key in seen: continue
                else: seen.append(key)
                rVal.append( (model,resi,diff) )
                # expand the selection here; I chose to iterate over stored.r instead of
                # creating one large selection b/c if there are too many residues PyMOL
                # might crash on a very large selection.  This is pretty much guaranteed
                # not to kill PyMOL; but, it might take a little longer to run.
                cmd.select( selName1, selName1 + " or (%s and i. %s)" % (model,resi))
        #
        # this is how you transfer a selection to another object.

        #cmd.select(selName, "(%s in %s) or (%s in %s)" % (receptor, selName1, peptide, selName1))
        # clean up after ourselves
        cmd.delete(selName1)
        cmd.delete(chP)
        cmd.delete(chR)
        cmd.delete(tempC)
        # show the selection
        #cmd.enable(selName)

        if len(rVal) > int(residCutoff):
            cmd.translate(vector, peptide, camera=0)
        else:
            cmd.alter(peptide, 'chain="A"')
            cmd.save("%s/out/%s-%s.pdb" % (pathPrefix, receptor, peptide), "%s or (%s and chain %s)" % (peptide, receptor, receptorChain))
            break
    #
    # reset users settings
    cmd.set("dot_solvent", oldDS)

    cmd.delete(peptide)

    return 0

for file in glob("%s/data/*.pdb" % pathPrefix):
    pdb_peptide = os.path.splitext(os.path.basename(file))[0]
    print("Working on %s" % pdb_peptide)
    dockPeptide(pdb_peptide)

cmd.extend("dockPeptide", dockPeptide)
