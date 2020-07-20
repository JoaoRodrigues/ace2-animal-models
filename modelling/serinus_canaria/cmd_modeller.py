#!/usr/bin/env python

from modeller import *
from modeller.automodel import *
from modeller.parallel import *
from fixatoms import MyModel_loop

j = job(host='localhost')
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())

log.verbose()
env = environ()

env.libs.topology.read(file='$(LIB)/top_heav.lib')
env.libs.parameters.read(file='$(LIB)/par.lib')
env.io.atom_files_directory = ['./']

# Read in HETATM records from template PDBs
env.io.hetatm = True

a = MyModel_loop(
    env,
    alnfile='ali_serinus_canaria.fasta',
    knowns=('6m17_BE_wSugar'),
    sequence='serinus_canaria',
    assess_methods=(assess.DOPE,),
    loop_assess_methods=(assess.DOPE,),
)

a.starting_model = 1
a.ending_model = 1
a.loop.starting_model = 1
a.loop.ending_model = 10
a.loop.md_level = refine.very_fast

# Optimization
# CG
a.library_schedule = autosched.fastest
a.max_var_iterations = 300
a.max_molpdf = 1e6

# MD
a.md_level = refine.very_fast

a.use_parallel_job(j)
a.make()


