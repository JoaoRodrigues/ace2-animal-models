#!/bin/bash

pdbdir=$1
[[ -z "$pdbdir" ]] && echo "usage: $0 pdb_dir" && exit 1

for pdb in $( ls ${pdbdir}/*pdb )
do
  species=$( basename $pdb | cut -d"_" -f1,2 )
  echo $species

  [[ -d "$species" ]] && rm -rf $species
  mkdir $species

  cp $pdb $species

  cd $species

  cp -r ../toppar/ .
  cp ../get_residue_score.inp .

  pdb_splitmodel.exe $( basename $pdb )

  rm -f molecule.pdb
  for model in $( ls *_best10_*.pdb )
  do
    echo $model
    cat $model > molecule.pdb
    echo "END" >> molecule.pdb

    cns < get_residue_score.inp > ${model%%.pdb}.cns.log
  done

  rm -rf toppar get_residue_score.inp molecule.pdb

  cd ../
done
