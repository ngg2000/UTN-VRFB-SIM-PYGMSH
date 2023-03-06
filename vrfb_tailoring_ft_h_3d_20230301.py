# ------------------------------------------------------------------------------
#
#  FLOW TRHOUGH FIELD 3D
#  2 CHANNELS
#  ELECTRODE INTRUSION AVAILABLE
#
# ------------------------------------------------------------------------------

import gmsh
import math
import sys

gmsh.initialize()

gmsh.model.add("electrodechannel")

#electrode
e_t = 0.00432         #electrode paper thickness
e_p = 0.00068             #electrode paper intrusion

#channels
ch_w = 0.002         #channel width
ch_d = 0.001          #channel depth 
ch_h = 0.003        #channel height
r_w = 0.03             #rib width

#ports 
p_l = 0.005         #port length
p_h = ch_h         #port height

#laser hole
h_d = 0.0001       #hole diameter
pos_hole = 0.5    #center of the hole position referred to the center of the channel


#depth of the first model size (this is going to be extruded)
el_s = 0.001

control_parameter_1 = 0.9*ch_w #control parameter: max position of the point (center of the hole + diameter of the hole)
control_parameter_2 = 0.1*ch_w #control parameter: min position of the point (center of the hole - diameter of the hole)

separation_center = el_s/2 #middle point of the element which separates one half-channel and another.
separation_semiwidth = 0.000375 #half of the distance between one half-channel and another.

#CODE SECURITY CONDITIONALS

if r_w/2+ch_w*pos_hole+h_d/2 >= r_w/2+control_parameter_1:
  pos_hole = 0.9*control_parameter_1/ch_w
  h_d = control_parameter_2
  print("Error: Excessive hole diameter. New hole diameter set by default")
elif ch_w*pos_hole >= control_parameter_1*0.95:
  pos_hole = 0.9*control_parameter_1/ch_w
  print("Error: Hole position near limit. New hole center and hole diameter set by default")


if r_w/2+ch_w*pos_hole-h_d/2 <= r_w/2+control_parameter_2:
  pos_hole = 2*control_parameter_2/ch_w
  h_d = control_parameter_2
  print("Error: Excessive hole diameter or hole position. New hole diameter and hole center set by default")
elif ch_w*pos_hole <= control_parameter_2:
  pos_hole = control_parameter_2*2
  print("Error: Hole position near limit. New hole center set by default")



a = gmsh.model.geo

#Points

z = [0, separation_center-separation_semiwidth, separation_center+separation_semiwidth, 2*separation_center]
#y = [0, -p_h, -e_p]
#x = [0, e_t, e_p, ch_h]


for k in range(0, 4, 1):
  a.addPoint(-ch_w-r_w/2,                                 0, z[k], el_s, 2+k*100)
  a.addPoint(-r_w/2,                                      0, z[k], el_s, 5+k*100)
  a.addPoint(-(ch_w*pos_hole + h_d) - r_w/2,              0, z[k], el_s, 3+k*100)
  a.addPoint(-(ch_w*pos_hole - h_d) - r_w/2,              0, z[k], el_s, 4+k*100)
  a.addPoint(r_w/2,                                       0, z[k], el_s, 6+k*100)
  a.addPoint((ch_w*pos_hole + h_d) + r_w/2,               0, z[k], el_s, 8+k*100)
  a.addPoint((ch_w*pos_hole - h_d) + r_w/2,               0, z[k], el_s, 7+k*100)
  a.addPoint(ch_w+r_w/2,                                  0, z[k], el_s, 9+k*100)
  a.addPoint(-ch_w-r_w/2-p_l,                             0, z[k], el_s, 1+k*100)
  a.addPoint(ch_w+r_w/2+p_l,                              0, z[k], el_s, 10+k*100)

#Z-axis lines

for i in range(len(z) - 1):
  for j in range(1, 11):
    a.addLine(j+i*100, j+(i+1)*100, j+(i*100))

#X-axis lines

for i in range(len(z)):
  for x in range(1, 10):
    a.addLine(x+i*100, (x+1)+i*100, (x + 10)+i*100)

#Loops and Surfaces

for i in range(1, 10):
  for k in range(len(z) - 1):
    a.addCurveLoop([i+k*100, (i + 10) + (k + 1)*100, -((i+1)+k*100), -((i + 10) + k*100)], i+k*100)
    a.addPlaneSurface([i+k*100], i+k*100)

#Extrusion and Volumes

#Extrusions in -Y axis (inlet, outlet)

inletblock = []

for i in range(1, 5):
  for k in range(len(z) - 1):
    inletblock.append(a.extrude([(2, i+k*100)], 0, -e_p, 0, recombine=True))

'''
inlet: i=1; electrode hole: i=3; electrode channel: i=2, i=4; k refers to elements in Z axis
PHYSICAL VOLUMES REMINDERS:
inlet: from inletblock[0] to inletblock[2]; electrode hole: from inletblock[6] to inletblock[8]
electrode channel: from inletblock[3] to inletblock[5] and from inletblock[9] to inletblock[11]
'''

outletblock = []

for i in range(6, 10):
  for k in range(len(z) - 1):
    outletblock.append(a.extrude([(2, i+k*100)], 0, -e_p, 0, recombine=True))

'''
outlet: i=9; electrode hole: i=7; electrode channel: i=6, i=8; k refers to elements in Z axis
PHYSICAL VOLUMES REMINDERS:
outlet: from outletblock[9] to inletblock[11]; electrode hole: from outletblock[3] to outletblock[5]
electrode channel: from outletblock[0] to outletblock[2] and from outletblock[6] to outletblock[8]
'''

#Extrusions in +Y axis (electrode rib and channel)

electrodeblock = []

for i in range(2, 9):
  for k in range(len(z) - 1):
    electrodeblock.append(a.extrude([(2, i+k*100)], 0, e_t, 0, recombine=True))

'''
electrode hole (inlet side): i=3; electrode channel(inlet side): i=2, i=4; 
electrode hole (outlet side): i=7; electrode channel (outlet side): i=6, i=8; k refers to elements in Z axis
PHYSICAL VOLUMES REMINDERS:
electrode rib: from electrodeblock[9] to electrodeblock[11]
(inlet side)
electrode hole: from electrodeblock[3] to electrodeblock[5]
electrode channel: from electrodeblock[0] to electrodeblock[2] and from electrodeblock[6] to electrodeblock[8]
(outlet side)
electrode hole: from electrodeblock[15] to electrodeblock[17]
electrode channel: from electrodeblock[12] to electrodeblock[14] and from electrodeblock[18] 
to electrodeblock[20]
'''

downoutletblock = []
downinletblock = []
for i in range(len(outletblock)):
  downoutletblock.append(a.extrude([(2, outletblock[i][0][1])], 0, -ch_h, 0, recombine=True))
  downinletblock.append(a.extrude([(2, inletblock[i][0][1])], 0, -ch_h, 0, recombine=True))

'''
Identify downinletblock[i] or downoutletblock[i] using the same rules from inletblock[i] or outletblock[i]
'''

gmsh.model.geo.synchronize()

#Physical volumes

fluidlist = []

for i in range(0, 3):
  fluidlist.append(inletblock[i][1][1])
for i in range(9, 12):
  fluidlist.append(outletblock[i][1][1])
for i in range(0, 12):
  fluidlist.append(downinletblock[i][1][1])
  fluidlist.append(downoutletblock[i][1][1])

gmsh.model.addPhysicalGroup(3, fluidlist, name="fluid")

holelist = []

for i in range(3, 6):
  holelist.append(electrodeblock[i][1][1])
  holelist.append(outletblock[i][1][1])
for i in range(6, 9):
  holelist.append(inletblock[i][1][1])
for i in range(15, 18):
  holelist.append(electrodeblock[i][1][1])

gmsh.model.addPhysicalGroup(3, holelist, name="hole")

intrusionlist = []

for i in range(0, 3):
  intrusionlist.append(outletblock[i][1][1])
for i in range(6, 9):
  intrusionlist.append(outletblock[i][1][1])
for i in range(3, 6):
  intrusionlist.append(inletblock[i][1][1])
for i in range(9, 12):
  intrusionlist.append(inletblock[i][1][1])

gmsh.model.addPhysicalGroup(3, intrusionlist, name="electrodeIntrusion")

channellist = []

for i in range(0, 3):
  channellist.append(electrodeblock[i][1][1])
for i in range(6, 9):
  channellist.append(electrodeblock[i][1][1])
for i in range(12, 15):
  channellist.append(electrodeblock[i][1][1])
for i in range(18, 21):
  channellist.append(electrodeblock[i][1][1])

gmsh.model.addPhysicalGroup(3, channellist, name="electrodeChannel")

riblist = []

for i in range(9, 12):
  riblist.append(electrodeblock[i][1][1])

gmsh.model.addPhysicalGroup(3, riblist, name="electrodeRib")

#Physical surfaces

inletlist = []

for i in range(0, 3):
  inletlist.append(inletblock[i][2][1])
  inletlist.append(downinletblock[i][2][1])

gmsh.model.addPhysicalGroup(2, inletlist, name="inlet")

outletlist = []

for i in range(9, 12):
  outletlist.append(outletblock[i][4][1])
  outletlist.append(downoutletblock[i][4][1])

gmsh.model.addPhysicalGroup(2, outletlist, name="outlet")

porouslist = []

for i in range(0, 3):
  porouslist.append(electrodeblock[i][2][1])
  porouslist.append(electrodeblock[i][0][1])
  porouslist.append(outletblock[i][2][1])
for i in range(3, 18):
  porouslist.append(electrodeblock[i][0][1])
for i in range(0, 3):
  porouslist.append(5 + i*100) #faces which where extruded cannot be identified with lists
for i in range(18, 21):
  porouslist.append(electrodeblock[i][4][1])
  porouslist.append(electrodeblock[i][0][1])
for i in range(9, 12):
  porouslist.append(inletblock[i][4][1])

gmsh.model.addPhysicalGroup(2, porouslist, name="wallsPorous")

wallslist = []

for i in range(0, 3):
  wallslist.append(1 + i*100)
  wallslist.append(9 + i*100)
  wallslist.append(downoutletblock[i][2][1])
for i in range(0, 12):
  wallslist.append(downinletblock[i][0][1])
  wallslist.append(downoutletblock[i][0][1])
for i in range(9, 12):
  wallslist.append(downinletblock[i][4][1])

gmsh.model.addPhysicalGroup(2, wallslist, name="walls")

frontbacklist = []

#Here i am using steps to capture only the front (or back). BECAUSE OF THE ORDER OF THE EXTRUDE LISTS, 3 and 5 are the indexes we use for this.
for i in range(0, 12, 3):
  frontbacklist.append(inletblock[i][5][1])
  frontbacklist.append(outletblock[i][5][1])
  frontbacklist.append(downinletblock[i][5][1])
  frontbacklist.append(downoutletblock[i][5][1])
for i in range(0, 21, 3):
  frontbacklist.append(electrodeblock[i][5][1])
for i in range(2, 12, 3):
  frontbacklist.append(inletblock[i][3][1])
  frontbacklist.append(outletblock[i][3][1])
  frontbacklist.append(downinletblock[i][3][1])
  frontbacklist.append(downoutletblock[i][3][1])
for i in range(2, 21, 3):
  frontbacklist.append(electrodeblock[i][3][1])

gmsh.model.addPhysicalGroup(2, frontbacklist, name="frontandBack")


#TRANSFINITE LINES IN X-AXIS DIRECTION

for i in range(1, 11, 1):
  for j in range(0, len(z)-1, 1):
    gmsh.model.mesh.setTransfiniteCurve(abs(i + j*100), 11, meshType="Progression", coef=0.80)

for i in range(11, 20, 1):
  for j in range(0, len(z), 1):
    gmsh.model.mesh.setTransfiniteCurve(abs(i + j*100), 11, meshType="Progression", coef=0.80)

for i in range(0, len(inletblock), 1):
  if i%3 == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  else:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=0.80)

for i in range(0, len(outletblock), 1):
  if i%3 == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  else:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=0.80)    

for i in range(0, len(electrodeblock), 1):
  if i%3 == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  else:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=0.80)

for i in range(0, len(downinletblock), 1):
  if i%3 == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  else:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=0.80)

for i in range(0, len(downoutletblock), 1):
  if i%3 == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  else:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=0.80)    


#TRANSFINITE LINES IN Y-AXIS DIRECTION

for i in range(0, len(downinletblock), 1):
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][2][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=0.80)
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][2][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
  if i >= ((len(downinletblock)) - 3):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][4][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][4][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=0.80)

for i in range(0, len(downoutletblock), 1):
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][2][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=0.80)
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][2][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
  if i >= ((len(downoutletblock)) - 3):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][4][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][4][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=0.80)

for i in range(0, len(outletblock), 1):
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][2][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=0.80)
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][2][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
  if i >= ((len(outletblock)) - 3):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][4][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][4][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=0.80)

for i in range(0, len(inletblock), 1):
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][2][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=0.80)
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][2][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
  if i >= ((len(inletblock)) - 3):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][4][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][4][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=0.80)

for i in range(0, len(electrodeblock), 1):
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][2][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=-0.80)
  gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][2][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=-0.80)
  if i >= ((len(electrodeblock)) - 3):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][4][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][4][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=-0.80)


#TRANSFINITE LINES IN Z-AXIS DIRECTION

for i in range(0, len(downinletblock), 1):
  if i == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=0.80)
  elif i > 0 and i < (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
  elif i == ((len(downinletblock)) - ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=-0.80)
  elif i > ((len(downinletblock)) -  ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  elif i >= (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downinletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)

for i in range(0, len(downoutletblock), 1):
  if i == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=0.80)
  elif i > 0 and i < (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
  elif i == ((len(downoutletblock)) - ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=-0.80)
  elif i > ((len(downoutletblock)) -  ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  elif i >= (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, downoutletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)

for i in range(0, len(inletblock), 1):
  if i == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=0.80)
  elif i > 0 and i < (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
  elif i == ((len(inletblock)) - ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=-0.80)
  elif i > ((len(inletblock)) -  ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  elif i >= (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, inletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)

for i in range(0, len(outletblock), 1):
  if i == 0:
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=0.80)
  elif i > 0 and i < (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[1][1], 11, meshType="Progression", coef=0.80)
  elif i == ((len(outletblock)) - ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[2][1], 11, meshType="Progression", coef=-0.80)
  elif i > ((len(outletblock)) -  ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[3][1], 11, meshType="Progression", coef=-0.80)
  elif i >= (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(gmsh.model.getBoundary(dimTags=[(2, outletblock[i][0][1])], oriented=True)[0][1], 11, meshType="Progression", coef=-0.80)

for i in range(0, len(electrodeblock), 1):
  if i == 0:
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[0][1]), 11, meshType="Progression", coef=0.80)
  elif i > 0 and i < (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[1][1]), 11, meshType="Progression", coef=0.80)
  elif i == ((len(electrodeblock)) - ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[0][1]), 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[2][1]), 11, meshType="Progression", coef=-0.80)
  elif i > ((len(electrodeblock)) -  ((len(z)) - 1)):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[0][1]), 11, meshType="Progression", coef=-0.80)
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[3][1]), 11, meshType="Progression", coef=-0.80)
  elif i >= (len(z) - 1):
    gmsh.model.mesh.setTransfiniteCurve(abs(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True)[0][1]), 11, meshType="Progression", coef=-0.80)

#print(electrodeblock)

#TRANSFINITE SURFACES, VOLUMES AND RECOMBINATION

for i in range(0, len(electrodeblock), 1):
  print(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][0][1])], oriented=True))

for i in range(0, len(electrodeblock), 1):
      print(gmsh.model.getBoundary(dimTags=[(2, electrodeblock[i][4][1])], oriented=True))

'''       "any"block[i][j][k] explanation 
----------------------------------------------------------------------------------------------------------------
· i represents the list generated by the extrusion of one face of the geometry. There are "i" faces extruded. As a
consequence of that, there are "i" lists.
· j represents the surface or volume within the "i"th list.
· if k=0, k represents the dimension of that entity - 2 for surface, 3 for volume.
· if k=1, k represents the tag of the entity contained in the "j"th tuple within the "i"th list. 
---------------------------------------------------------------------------------------------------------------- 
'''

for i in range(1, 10, 1):
  for j in range(0, len(z)-1, 1):
    gmsh.model.mesh.setTransfiniteSurface((i+j*100))
    gmsh.model.mesh.setRecombine(2, (i+j*100))

for i in range(0, len(inletblock), 1):
  for j in range(0, 6, 1):
    if inletblock[i][j][0] == 2:
      gmsh.model.mesh.setTransfiniteSurface(inletblock[i][j][1])
      gmsh.model.mesh.setRecombine(2, inletblock[i][j][1])
    elif inletblock[i][j][0] == 3:
      gmsh.model.mesh.setTransfiniteVolume(inletblock[i][j][1])

for i in range(0, len(downinletblock), 1):
  for j in range(0, 6, 1):
    if downinletblock[i][j][0] == 2:
      gmsh.model.mesh.setTransfiniteSurface(downinletblock[i][j][1])
      gmsh.model.mesh.setRecombine(2, downinletblock[i][j][1])
    elif downinletblock[i][j][0] == 3:
      gmsh.model.mesh.setTransfiniteVolume(downinletblock[i][j][1])

for i in range(0, len(outletblock), 1):
  for j in range(0, 6, 1):
    if outletblock[i][j][0] == 2:
      gmsh.model.mesh.setTransfiniteSurface(outletblock[i][j][1])
      gmsh.model.mesh.setRecombine(2, outletblock[i][j][1])
    elif outletblock[i][j][0] == 3:
      gmsh.model.mesh.setTransfiniteVolume(outletblock[i][j][1])

for i in range(0, len(downoutletblock), 1):
  for j in range(0, 6, 1):
    if downoutletblock[i][j][0] == 2:
      gmsh.model.mesh.setTransfiniteSurface(downoutletblock[i][j][1])
      gmsh.model.mesh.setRecombine(2, downoutletblock[i][j][1])
    elif downoutletblock[i][j][0] == 3:
      gmsh.model.mesh.setTransfiniteVolume(downoutletblock[i][j][1])

for i in range(0, len(electrodeblock), 1):
  for j in range(0, 6, 1):
    if electrodeblock[i][j][0] == 2:
      gmsh.model.mesh.setTransfiniteSurface(electrodeblock[i][j][1])
      gmsh.model.mesh.setRecombine(2, electrodeblock[i][j][1])
    elif electrodeblock[i][j][0] == 3:
      gmsh.model.mesh.setTransfiniteVolume(electrodeblock[i][j][1])

#MESH GENERATION

gmsh.model.mesh.generate(1)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.generate(3)

gmsh.write("vrfb_tailoring_ft_h_3d.msh")

gmsh.fltk.run()
gmsh.finalize()
