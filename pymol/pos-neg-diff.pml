# 60 mm @ 300dpi = 709px

set hash_max, 450
set max_threads, 10

load energy_analysis_5A_intra/homo_sapiens/homo_sapiens_ensemble_best10_0.pdb, human
load energy_analysis_5A_intra/mus_musculus/mus_musculus_ensemble_best10_0.pdb, mouse
load energy_analysis_5A_intra/anas_platyrhynchos/anas_platyrhynchos_ensemble_best10_0.pdb, duck

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
enable human

distance measure01, human and chain B and resi 30 and name OD2, human and chain E and resi 417 and name NZ
hide label

png human_B30.png, 709, 709, ray=1, dpi=300
delete measure01

disable all
enable mouse
png mouse_B30.png, 709, 709, ray=1, dpi=300

# Resi 31
hide sticks
show sticks, resi 31+35 and chain B
show sticks, resi 493 and chain E

set_view (\
    -0.281282067,    0.952944338,    0.112917356,\
    -0.722922027,   -0.287813485,    0.628113568,\
     0.631060421,    0.095051236,    0.769871831,\
     0.000331291,   -0.000546493,  -45.933895111,\
    22.576265335,   12.279696465,   -2.015512228,\
   -17.476818085,  109.414871216,  -20.000000000 )

disable all
enable human

distance measure01, human and chain B and resi 31 and name NZ, human and chain E and resi 493 and name OE1
distance measure02, human and chain B and resi 35 and name OE1, human and chain E and resi 493 and name NE2
hide label

png human_B31.png, 709, 709, ray=1, dpi=300

delete measure01
delete measure02

disable all
enable duck

distance measure01, duck and chain B and resi 31 and name OE2, duck and chain B and resi 35 and name NH2
hide label

png duck_B31.png, 709, 709, ray=1, dpi=300
delete measure01

# Resi 353
set cartoon_side_chain_helper, 0  # for this only

hide sticks
show sticks, resi 38+353 and chain B
show sticks, resi 496+502 and chain E

set_view (\
     0.013468108,    0.965335429,   -0.260576665,\
    -0.946933448,   -0.071371704,   -0.313351482,\
    -0.321095556,    0.250974208,    0.913165987,\
     0.000157987,   -0.000885531,  -56.962219238,\
    20.402601242,    5.953774452,    0.233211040,\
    -6.463727474,  120.427917480,  -20.000000000 )

disable all
enable human

distance measure01, human and chain B and resi 38 and name OD2, human and chain B and resi 353 and name NZ
distance measure02, human and chain B and resi 353 and name NZ, human and chain E and resi 496 and name O
distance measure03, human and chain B and resi 353 and name O, human and chain E and resi 502 and name N

hide label

png human_B353.png, 709, 709, ray=1, dpi=300
delete measure01
delete measure02
delete measure03

disable all
enable mouse

distance measure01, mouse and chain B and resi 353 and name O, mouse and chain E and resi 502 and name N
hide label

png mouse_B353.png, 709, 709, ray=1, dpi=300

set cartoon_side_chain_helper, 1  # reset

quit