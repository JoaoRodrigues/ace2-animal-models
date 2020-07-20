#!/usr/bin/env python

"""
Collects energy files from subfolders and makes a matrix.
"""

import argparse
import collections
import pathlib
import sys

import numpy as np


def read_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        'rootdir',
        type=pathlib.Path,
        help='Top-level folder to search for energy files.'
    )
    return ap.parse_args()


def collect_data(args):

    data = {}  # species: resi: vdw/elec/desolv

    rootdir = args.rootdir
    for file in rootdir.rglob('*.resene*'):

        energies = parse_energy_file(file)

        species = file.parent.stem
        if species not in data:
            data[species] = energies
        else:  # aggregate
            for res in energies:
                if res in data[species]:
                    data[species][res][0].extend(energies[res][0])
                    data[species][res][1].extend(energies[res][1])
                    data[species][res][2].extend(energies[res][2])
                else:
                    data[species][res] = energies[res]

    return data


def parse_energy_file(fpath):
    # ## Interface Residue Energies ("molecule.pdb")
    # ## Seg Res vdW Elec Desolv
    # B 24 GLU -3.44623 -32.1481 2.77849
    # B 27 LYS -3.79747 -28.3228 3.29628
    energies = {}  # resid: vdw/elec/desolv

    with fpath.open('rt') as handle:
        for line in handle:
            if line.startswith('#'):
                continue

            segid, resid, _, vdw, elec, desolv = line.split()
            if (segid, resid) in energies:
                raise Exception(f'duplicated: {segid}{resid} on {fpath}')
            
            energies[(segid, resid)] = [
                [float(vdw)],
                [float(elec)],
                [float(desolv)]
            ]

    return energies


def aggregate(datadict):

    # Produce an aggregate dict per species
    sorted_r = []
    for chain in ['B', 'E']:
        # agg resid
        resids = {
            r for s in datadict
            for r in datadict[s]
            if r[0] == chain
        }

        sorted_r.extend(sorted(resids, key=lambda x: int(x[1])))

    dataagg = {}
    # Now iterate by species
    # First make average per residue per species
    for s in datadict:

        rdict = {
            k: {'vdw': 0.0, 'elec': 0.0, 'desolv': 0.0, 'hs': 0.0}
            for k in sorted_r
        }
        dataagg[s] = rdict
        
        for r in sorted_r:
            if r not in datadict[s]:
                continue

            # make average
            vdw, elec, desolv = datadict[s][r]
            vdw = sum(vdw) / len(vdw)
            elec = sum(elec) / len(elec)
            desolv = sum(desolv) / len(desolv)
            hs = vdw + 0.2*elec + desolv

            dataagg[s][r]['vdw'] = vdw
            dataagg[s][r]['elec'] = elec
            dataagg[s][r]['desolv'] = desolv
            dataagg[s][r]['hs'] = hs

    # Now make csv file
    # Resids as columns
    # Species as rows
    species = sorted(datadict)

    for ene in ('vdw', 'elec', 'desolv', 'hs'):
        with open(f'agg_{ene}.csv', 'w') as handle:
            header = ['species'] + [''.join(i) for i in sorted_r]
            print(','.join(header), file=handle)
            for si, s in enumerate(species):
                row = [s] + [str(dataagg[s][r][ene]) for r in sorted_r]
                print(','.join(row), file=handle)
    return dataagg


if __name__ == '__main__':
    args = read_args()
    data = collect_data(args)
    aggdata = aggregate(data)