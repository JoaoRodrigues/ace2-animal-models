"""
Calculate sequence similarity for ACE2 orthologs based on an
input alignment file and an input PDB file of the ACE2:RBD complex
"""

import argparse
import pathlib
import re

from Bio.Data.IUPACData import protein_letters_3to1 as three_to_one
from Bio.PDB import PDBParser
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio import SeqIO

sim_mtx = {
    'R': 1, 'K': 1, 'H': 1,  # charged +
    'D': 2, 'E': 2,  # charged -
    'Y': 3, 'F': 3, 'Y': 3, 'W': 3,  # aromatic
    'S': 4, 'T': 4, 'N': 4, 'Q': 4,  # polar
    'A': 5, 'V': 5, 'I': 5, 'L': 5, 'M': 5,  # apolar
    'C': 6,
    'G': 7,
    'P': 8,
    '-': 0,
    'X': 0
}

##
parser = argparse.ArgumentParser()
parser.add_argument('-aln', required=True, type=pathlib.Path, help='Alignment')
parser.add_argument('-pdb', required=True, type=pathlib.Path, help='Reference PDB')
args = parser.parse_args()

# Read PDB
p = PDBParser(QUIET=1)
pdb = p.get_structure(
    'reference',
    str(args.pdb.resolve(strict=True))
)
pdb = pdb[0]  # only one model
print('Read reference PDB file')

# Get interface residues for chain B
ace2_interface = []
ns = NeighborSearch(list(pdb.get_atoms()))
neighbors = ns.search_all(5.0, 'R')  # all res pairs within 5A
for r1, r2 in neighbors:
    c1, c2 = r1.parent.id, r2.parent.id
    if c1 == c2:
        continue

    if c1 == 'B':
        ace2_interface.append(r1)
    elif c2 == 'B':
        ace2_interface.append(r2)

ace2_interface = {r.id[1] for r in ace2_interface if r.id[0] == ' '}
print(f'Computed {len(ace2_interface)} interface residues')

# Map to alignment
pdb_aln_map = {}

aln = list(SeqIO.parse(args.aln, format='fasta'))
refe = aln[0]
refeseq = str(refe.seq)
pdbres = [r for r in pdb['B'].child_list if r.id[0] == ' ']  # no het
gaps = set()

for idx, aa in enumerate(refeseq):
    if aa == '-':
        gaps.add(idx)
        continue

    pdb_aa = pdbres.pop(0)
    pdb_aln_map[idx] = pdb_aa

pdb_to_name = {
    i: three_to_one[pdb_aa.resname.capitalize()]
    for i, pdb_aa in pdb_aln_map.items()
}

# Now go over alignment and calculate similarities
n_aa = len(pdb_aln_map)  # do not count gaps!
n_i_aa = len(ace2_interface)

re_species = re.compile(r'\[.*\]')

for entry in aln:
    spname = re_species.findall(entry.description)
    if spname:
        spname = spname[0][1:-1]
    else:
        spname = entry.description

    alnseq = str(entry.seq)

    id_g = 100 * sum([
        aa == pdb_to_name[i] for i, aa in enumerate(alnseq) if i not in gaps
    ]) / n_aa

    id_i = 100 * sum([
        aa == pdb_to_name[i] for i, aa in enumerate(alnseq)
        if i not in gaps and pdb_aln_map[i].id[1] in ace2_interface
    ]) / n_i_aa

    sim_g = 100 * sum([
        sim_mtx[aa] == sim_mtx[pdb_to_name[i]]
        for i, aa in enumerate(alnseq) if i not in gaps
    ]) / n_aa

    sim_i = 100 * sum([
        sim_mtx[aa] == sim_mtx[pdb_to_name[i]] for i, aa in enumerate(alnseq)
        if i not in gaps and pdb_aln_map[i].id[1] in ace2_interface
    ]) / n_i_aa

    print(f'{spname:<30s},{id_g:4.1f},{id_i:4.1f},{sim_g:4.1f},{sim_i:4.1f}')
