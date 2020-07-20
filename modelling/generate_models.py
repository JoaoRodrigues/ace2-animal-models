"""
Generates models of ACE2 for a list of species.
"""

import argparse
import collections
import os
import pathlib
import shutil
import subprocess
import sys


def read_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--template',
        help='Template PDB structure',
        required=True
    )
    ap.add_argument(
        '--sequences',
        help='Aligned sequences',
        required=True
    )
    ap.add_argument(
        '--species-list',
        help='List of species',
        required=True
    )
    return ap.parse_args()


def fetch_sequences(seqfile, specfile):
    species = []
    with open(specfile) as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            species.append(line)
    print(f'Collected {len(species)} species from file: {specfile}')

    seqdict = {}  # species -> seq
    fastaseq = []
    specname = None
    with open(seqfile) as handle:
        for line in handle:
            line = line.strip()
            if line.startswith('>'):
                if fastaseq:
                    fastaseq = ''.join(fastaseq)
                    fastaseq = fastaseq.replace('X', 'G')
                    seqdict[specname] = fastaseq
                    fastaseq = []

                # Match species name
                for s in species[:]:
                    if s.lower() in line.lower():
                        specname = s
                        species.remove(s)
                        break
                else:
                    specname = None

            elif specname is not None:
                fastaseq.append(line)

    if fastaseq:
        fastaseq = ''.join(fastaseq)
        fastaseq = fastaseq.replace('X', 'G')
        seqdict[specname] = fastaseq

    if species:
        print('Species Missing')
        for s in species:
            print(f'\t{s}')

    return seqdict


def make_models(seqs, pdb_template):
    
    for seqname, fastaseq in seqs.items():
        print(f'{seqname} >>')
        seqname = '_'.join(seqname.lower().split()).strip('_')

        # Make fastaseq 60chars per line
        _f = []
        for i in range(0, len(fastaseq), 60):
            _f.append(fastaseq[i: i+60])
        fastaseq = _f

        # Do we have gaps? -> loopmodel
        cmdmodeller = 'cmd_modeller_bb.py'

        len_seq = len([c for c in ''.join(fastaseq) if c != '-'])
        if len_seq > 580:  # reference
            print(f'  loopmodel: {len_seq} > 580')
            cmdmodeller = 'cmd_modeller_loops.py'

        sdir = pathlib.Path(seqname)
        try:
            sdir.mkdir()
        except FileExistsError:
            print('skipping')
            continue
            # shutil.rmtree(str(sdir))
            # sdir.mkdir()

        # Make ali fasta
        with open('ali.fasta', 'r') as template:
            fpath = sdir / f'ali_{seqname}.fasta'
            with fpath.open('wt') as outhandle:
                t = template.read().replace(
                    'SEQNAME', seqname
                ).replace(
                    'SEQFASTA', '\n'.join(fastaseq)
                )
                print(t, file=outhandle)

        # Make cmd_modeller.py
        with open(cmdmodeller, 'r') as template:
            fpath = sdir / 'cmd_modeller.py'
            with fpath.open('wt') as outhandle:
                t = template.read().replace(
                    'SEQNAME', seqname
                )
                print(t, file=outhandle)

        fpath = sdir / 'fixatoms.py'
        shutil.copyfile('fixatoms.py', str(fpath))

        # Copy template
        fpath = sdir / '6m17_BE_wSugar.pdb'
        shutil.copyfile('6m17_BE_wSugar.pdb', str(fpath))

        # Launch modeller
        os.chdir(str(sdir))
        print('\tRunning MODELLER')
        with open('modeller.log', 'w') as logfile:
            with open('modeller.err', 'w') as logerr:
                p = subprocess.Popen(
                    'python cmd_modeller.py',
                    shell=True,
                    stdout=logfile,
                    stderr=logerr,
                    close_fds=True
                )
                p.communicate()

        os.chdir('..')


if __name__ == '__main__':
    args = read_args()
    seqs = fetch_sequences(
        args.sequences,
        args.species_list
    )

    make_models(
        seqs,
        args.template
    )
