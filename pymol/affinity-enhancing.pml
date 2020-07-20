# 45 mm at 300 dpi, 531px

set hash_max, 450
set max_threads, 10

load energy_analysis_5A_intra/homo_sapiens/homo_sapiens_ensemble_best10_0.pdb, human
load energy_analysis_5A/rhinolophus_sinicus/rhinolophus_sinicus_ensemble_best10_0.pdb, bat
load energy_analysis_5A/canis_lupus/canis_lupus_familiaris_ensemble_best10_0.pdb, dog
load energy_analysis_5A/bos_taurus/bos_taurus_ensemble_best10_0.pdb, cow
load energy_analysis_5A/mustela_putorius/mustela_putorius_furo_ensemble_best10_5.pdb, ferret

# Align on human ACE2
alignto human and chain B and name CA

# Remove Hs and Glycans
remove hydro
remove resi 900-

# General Style
set_color nitrogen, [41, 75, 122]
set_color oxygen, [163, 20, 32]
set_color ace2, [241, 250, 238]
set_color rbd, [168, 218, 220]

color ace2, chain B
color rbd, chain E
util.cbaw not elem C
color nitrogen, elem N
color oxygen, elem O

show cartoon
cartoon tube
set cartoon_tube_radius, 0.8
set cartoon_tube_quality, 50
set stick_radius, 0.5
set valence, 0
set cartoon_side_chain_helper, 1


set dash_width, 8.0
set dash_gap, 0

set light_count, 8
set spec_count, 0
set shininess, 0
set specular, 0
set ambient, 0.4
set direct, 0.5
set reflect, 0.2

# Ray
bg white
set fog_start, 0.45
set ray_opaque_background, 0
set ray_trace_mode, 1
set ray_trace_disco_factor, 1.0
set ray_trace_gain, 0.6
set antialias, 3
set ray_shadow, 0

#
# Now show and ray trace sites one by one.

# Resi 24
hide sticks
show sticks, resi 24+21 and chain B
show sticks, resi 487 and chain E

set_view (\
    -0.066165924,    0.992097676,   -0.106596127,\
    -0.170419306,    0.094021261,    0.980867028,\
     0.983135939,    0.083065681,    0.162848771,\
     0.000000000,    0.000000000,  -31.038944244,\
    20.008121490,   22.411052704,  -10.357009888,\
   -43.326374054,  105.404289246,  -20.000000000 )

disable all
enable human

distance measure01, human and chain B and resi 24 and name NE2, human and chain E and resi 487 and name OD1
hide label

png human_B24.png, 531, 531, ray=1, dpi=300
delete measure*

disable all
enable bat
set cartoon_side_chain_helper, 0

distance measure01, bat and chain B and resi 24 and name OE2, bat and chain E and resi 487 and name ND2
distance measure02, bat and chain B and resi 24 and name OE1, bat and chain B and resi 21 and name N
hide label

png bat_B24.png, 531, 531, ray=1, dpi=300
delete measure*

set cartoon_side_chain_helper, 1

# Resi 25

hide cartoon, resi -23
hide sticks
show sticks, resi 25 and chain B
show sticks, resi 29+83+97 and chain B

set_view (\
    -0.101978563,    0.961377919,    0.255629301,\
     0.956660867,    0.024323486,    0.290167928,\
     0.272743255,    0.274142176,   -0.922197700,\
    -0.000157920,   -0.000069564,  -25.087430954,\
    14.362728119,   19.278249741,  -10.522875786,\
    -9.234054565,   58.893321991,  -20.000000000 )

disable all
enable human

distance measure01, human and chain B and resi 25 and name CB, human and chain B and resi 29 and name CD1
distance measure02, human and chain B and resi 25 and name CB, human and chain B and resi 83 and name CD2
distance measure03, human and chain B and resi 25 and name CB, human and chain B and resi 97 and name CD1

hide label

png human_B35.png, 531, 531, ray=1, dpi=300
delete measure*

disable all
enable dog

distance measure01, dog and chain B and resi 25 and name CG1, dog and chain B and resi 29 and name CD1
distance measure02, dog and chain B and resi 25 and name CG1, dog and chain B and resi 29 and name CD2
distance measure03, dog and chain B and resi 25 and name CG2, dog and chain B and resi 83 and name CE1
distance measure04, dog and chain B and resi 25 and name CG1, dog and chain B and resi 97 and name CD1
hide label

png dog_B25.png, 531, 531, ray=1, dpi=300
delete measure*

show cartoon  # restore

# Resi 30
hide sticks
show sticks, resi 30 and chain B
show sticks, resi 417 and chain E

set_view (\
    -0.016222704,    0.915790737,    0.401298225,\
     0.605398297,   -0.310423851,    0.732881367,\
     0.795744956,    0.254840344,   -0.549383700,\
     0.000000000,    0.000000000,  -34.037582397,\
    23.167499542,   10.569499969,   -6.845000267,\
   -29.408308029,   97.483467102,  -20.000000000 )

disable all
enable cow

distance measure01, cow and chain B and resi 30 and name OE2, cow and chain E and resi 417 and name NZ
hide label

png cow_B30.png, 531, 531, ray=1, dpi=300
delete measure*

# Resi 387
hide sticks
show sticks, resi 387+354 and chain B
show sticks, resi 408 and chain E

set_view (\
     0.140235320,    0.980235219,    0.139528930,\
     0.000386809,    0.140863597,   -0.990009844,\
    -0.990098596,    0.138888985,    0.019377224,\
    -0.000273219,   -0.000049380,  -44.988651276,\
    17.233118057,   -0.626366138,   -6.399028301,\
    18.826738358,   71.134971619,  -20.000000000 )

disable all
enable human

png human_B387.png, 531, 531, ray=1, dpi=300

disable all
enable ferret

distance measure01, ferret and chain B and resi 387 and name OE1, ferret and chain B and resi 354 and name NH2
distance measure02, ferret and chain B and resi 387 and name OE2, ferret and chain E and resi 408 and name NH1
hide label

png ferret_B387.png, 531, 531, ray=1, dpi=300
delete measure*

quit