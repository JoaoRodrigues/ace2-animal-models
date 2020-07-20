# Modeling Protocol

Requires MODELLER.

## Use modeller and 6m17_BE to generate models of ACE2 (bound to S)
```bash
python generate_models.py --template templates/6m17_BE_wSugar.pdb \
                          --sequences ../sequences/ACE2_refseq_aln.mafft_trimmed_6m17.fasta \
                          --species-list ../sequences/species-of-interest.txt
```

## Process models to match numbering of 6m17 and remove sugars when Asn is mutated.
```bash
cd homo_sapiens  # example
python process_models.py 6m17_BE_wSugar.pdb ali*fasta
```
