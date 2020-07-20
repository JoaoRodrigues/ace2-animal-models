"""
Batch script to prepare complexes for docking.

(1) Renumbers models based on the original template and an alignment.
(2) Removes NAGs where ASNs are not conserved
"""

import argparse
import pathlib
import sys

from Bio.PDB import PDBIO
from Bio.PDB import PDBParser
from Bio.PDB.NeighborSearch import NeighborSearch

from modeller import *


ap = argparse.ArgumentParser()
ap.add_argument('template')
ap.add_argument('alignment')
args = ap.parse_args()

curdir = pathlib.Path('.')
dirname = curdir.resolve().stem

mdl_root = dirname
template_name = '6m17_BE_wSugar'

log.level(output=1, notes=1, warnings=1, errors=1, memory=0)
env = environ()

env.libs.topology.read(file='$(LIB)/top_heav.lib')
env.libs.parameters.read(file='$(LIB)/par.lib')

# directories for input atom files
# env.io.atom_files_directory = './'

# Read in HETATM records from template PDBs
env.io.hetatm = True

# Read an alignment for the transfer
aln = alignment(
    env,
    file=args.alignment,
    align_codes=[mdl_root, template_name]
)

# Pick the lowest energy model (DOPE)
lowest_score = sys.maxsize
mdl = None
for mdl_fpath in curdir.glob(f'{mdl_root}.B*.pdb'):

    with open(mdl_fpath) as handle:
        _mdl = model(env, file=handle)
        z_dope = _mdl.assess_normalized_dope()
        if z_dope < lowest_score:
            mdl = _mdl
            lowest_score = z_dope

assert mdl is not None

print(f'picked model: {mdl.last_energy}')

# Read the template and target models:

template = aln[template_name]
numbering = []

# Transfer the residue and chain ids
# If the residue is not in the template,
# increment from the last residue and add 5000.
for mdl_res, aln_res in zip(mdl.residues, aln[mdl_root].residues):

    t_res = aln_res.get_aligned_residue(template)
    if t_res is None:  # model insertion
        # Use info from last one and increase by 5000
        t_res_num, t_res_chain = numbering[-1]
        t_res_num_int = int(t_res_num)
        if t_res_num_int < 5000:
            t_res_num_int += 5000

        t_res_num_int += 1
        t_res_num = str(t_res_num_int)
    else:  # copy from template
        t_res_num = t_res.num
        t_res_chain = t_res.chain.name
    # print(mdl_res, t_res_num, t_res_chain)
    mdl_res.num = t_res_num
    mdl_res.chain.name = t_res_chain
    numbering.append((t_res_num, t_res_chain))

# Save file
fpath = pathlib.Path(mdl_fpath)
rootname = fpath.stem
mdl.write(file=f'{rootname}_renum.pdb')

# Delete sugars
parser = PDBParser(QUIET=1)
io = PDBIO()

mdl = parser.get_structure(
    f'{rootname}_renum',
    f'{rootname}_renum.pdb'
)

bound_nags = set()
for model in mdl:
    ns = NeighborSearch(list(model.get_atoms()))
    nags = [
        r for r in model.get_residues()
        if r.resname == 'NAG' and r.parent.id == 'B'
    ]

    # 1st pass
    for nag in nags:
        c1_nag = nag['C1']
        for n in ns.search(c1_nag.coord, 3.5, 'A'):
            if n.parent.resname == 'ASN' and n.name == 'ND2':
                bound_nags.add(nag.id[1])
                break

    # 2nd pass
    for nag in nags:
        c1_nag = nag['C1']
        for n in ns.search(c1_nag.coord, 3.5, 'A'):
            if n.parent.resname == 'NAG' and n.parent.id[1] != nag.id[1] and n.name == 'O4' and n.parent.id[1] in bound_nags:
                bound_nags.add(nag.id[1])
                break

all_nags = {
    r.id[1] for r in model.get_residues()
    if r.resname == 'NAG' and r.parent.id == 'B'
}  # scan last model for total NAGs
unbound_nags = all_nags - bound_nags

for resid in sorted(unbound_nags):
    print(f'Removing NAG {resid}')
    for model in mdl:
        ace2 = model['B']
        res = ace2[('H_NAG', resid, ' ')]
        ace2.detach_child(res.id)


io.set_structure(mdl)
io.save(f'{dirname}_ensemble.pdb')

assert pathlib.Path(f'{dirname}_ensemble.pdb').resolve(strict=True)
