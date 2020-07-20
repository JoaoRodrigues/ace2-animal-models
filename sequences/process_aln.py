"""
Filters alignment for species of interest and removes
100% gapped columns.

usage: process_aln.py alignment.fasta species.list
"""

import sys

# Read seqs
ids, seqs = [], []
with open(sys.argv[1]) as handle:
    seq = []
    for line in handle:
        if line.startswith('>'):
            if seq:
                seqs.append(''.join(seq))
                seq = []
            ids.append(line.strip())
        elif line.strip():
            seq.append(line.strip())

if seq:
    seqs.append(''.join(seq))

manual = []  # fill here species you dont want

# read species list
with open(sys.argv[2]) as handle:
    species = []
    for line in handle:
        if line.startswith('#'):
            continue
        for m in manual:
            if m in line:
                break
        else:
            species.append(f'[{line.strip()}]')

species.insert(0, '6M17')

marked = []
for s in species:
    for idx, i in enumerate(ids):
        if s in i:
            marked.append(idx)

marked = set(marked)
ids = [ids[i] for i in range(len(ids)) if i in marked]
seqs = [seqs[i] for i in range(len(seqs)) if i in marked]


# Remove gaps present in ALL sequences
refseq = seqs[0]
n_seqs = len(seqs)
n_aa = len(refseq)

gaps = [0 for _ in range(n_aa)]
for seq in seqs:
    for idx, aa in enumerate(seq):
        if aa == '-':
            gaps[idx] += 1

# Add gaps before PDB and after PDB sequence
first, last = None, None
for idx, aa in enumerate(refseq):
    if aa != '-':
        first = idx
        break
for idx, aa in enumerate(refseq[::-1]):
    if aa != '-':
        last = n_aa - idx - 1
        break

gapidx = {
    i for i, c in enumerate(gaps)
    if (c == n_seqs) or (i < first) or (i > last)
}

# Write ungapped aln
for seq_id, seq in zip(ids, seqs):
    ungapped = ''.join(c for i, c in enumerate(seq) if i not in gapidx)
    print(f'{seq_id}\n{ungapped}')
