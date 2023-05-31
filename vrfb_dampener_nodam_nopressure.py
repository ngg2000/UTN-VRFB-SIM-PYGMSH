#----------------------------------------
#
# PULSATION DAMPENER SIZING
# 
# FLOW THROUGH FIELD 2D
#
#----------------------------------------

#GMSH INIT

import gmsh
import math
import sys

gmsh.initialize()

gmsh.model.add("fluid_dampener")

#INPUTS

#x_anything: dimensions of the object along x-axis
#y_anything: dimensions of the object along y-axis

##geometry parameters
extrusion_z = 1

l_inlet = 50
w_inlet = 10
inlet_pos = 0 #position of the middle of the inlet, in percent of w_vol. Goes from -0.5 to +0.5

l_vol = 50
w_vol = 50

l_dam = 15
w_dam = 10
dam_pos = 0.35 #position of the middle of the dam, in percent of l_vol

l_outlet = 50
w_outlet = 10
outlet_pos = 0.75 #position of the middle of the outlet, in percent of l_vol

l_pressure_inlet = 15
w_pressure_inlet = 10
pressure_inlet_pos = 0.5 #position of the middle of the pressure tap, in percent of l_inlet.

l_pressure_outlet = 15
w_pressure_outlet = 10
pressure_outlet_pos = 0.5 #position of the middle of the pressure tap, in percent of l_outlet.

l_tube = 250
w_tube = 45
##Spacings
###Horizontal Lines: the same spacing and amount of elements for the horizontal lines between two vertical lines. 
inlet_left_hor_sp = 0.3
inlet_left_hor_el = 11
inlet_left_hor_type = "Bump"

inlet_center_hor_sp = 0.6
inlet_center_hor_el = 9
inlet_center_hor_type = "Bump"

pressure_inlet_hor_sp = 0.4
pressure_inlet_hor_el = 13
pressure_inlet_hor_type = "Bump"

inlet_right_hor_sp = 0.3
inlet_right_hor_el = 11
inlet_right_hor_type = "Bump"

inlet_outlet_hor_sp = 0.8
inlet_outlet_hor_el = 11
inlet_outlet_hor_type = "Bump"

tube_left_sp = 0.08
tube_left_el = 22
tube_left_type = "Bump"

tube_right_sp = 0.08
tube_right_el = 22
tube_right_type = "Bump"
###Vertical lines: same logic as horizontal lines.

inlet_begin_ver_el = 11
inlet_begin_ver_sp = 0.35
inlet_begin_ver_type = "Bump"

inlet_pressure_ver_el = 8
inlet_pressure_ver_sp = 0.8
inlet_pressure_ver_type = "Bump"

inlet_end_ver_el = 11
inlet_end_ver_sp = 0.6
inlet_end_ver_type = "Bump"

vol_inlet_ver_el = 20
vol_inlet_ver_sp = 0.75
vol_inlet_ver_type = "Bump"

vol_dam_ver_el = 11
vol_dam_ver_sp = 0.8
vol_dam_ver_type = "Bump"

vol_middle_ver_el = 11
vol_middle_ver_sp = 0.8
vol_middle_ver_type = "Bump"

vol_outlet_ver_el = 9
vol_outlet_ver_sp = 0.85
vol_outlet_ver_type = "Bump"

vol_end_ver_el = 7
vol_end_ver_sp = 0.9
vol_end_ver_type = "Bump"

tube_ver_el = 22
tube_ver_sp = 0.3
tube_ver_type = "Bump"

#POINTS: tags conveniently created to optimize the creation of the lines

a = gmsh.model.geo
el_s = 0.001 

#Axis origin: in the middle of the beggining of the inlet.
#X-axis: positive in the direcion of the outlet
#Y-axis: positive going from the inlet to the outlet.
#Z-axis: positive using the right-hand rule.

a.addPoint(w_vol*inlet_pos + w_inlet/2, 0, 0, el_s, 2) #beggining of the inlet, depending on the inlet_pos parameter
a.addPoint(w_vol*inlet_pos - w_inlet/2, 0, 0, el_s, 1)
a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet*pressure_inlet_pos + w_pressure_inlet/2, 0, el_s, 6) #pressure tap definition, depending on the pressure_inlet_pos parameter
a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet*pressure_inlet_pos - w_pressure_inlet/2, 0, el_s, 3)
#a.addPoint(w_vol*inlet_pos + w_inlet/2 + l_pressure_inlet, l_inlet*pressure_inlet_pos + w_pressure_inlet/2, 0, el_s, 5)
#a.addPoint(w_vol*inlet_pos + w_inlet/2 + l_pressure_inlet, l_inlet*pressure_inlet_pos - w_pressure_inlet/2, 0, el_s, 4)

a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet, 0, el_s, 7) #end of the inlet
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet, 0, el_s, 26)

a.addPoint(w_vol/2, l_inlet, 0, el_s, 8) #beggining of the vol
a.addPoint(-w_vol/2, l_inlet, 0, el_s, 25)

a.addPoint(w_vol/2, l_inlet + l_vol*outlet_pos - w_outlet/2, 0, el_s, 9) #outlet definition: beggining
a.addPoint(w_vol/2, l_inlet + l_vol*outlet_pos + w_outlet/2, 0, el_s, 18)

a.addPoint(-l_tube/2, 0, 0, el_s, 10)
a.addPoint(-l_tube/2, -w_tube, 0, el_s, 11) #tube definition
a.addPoint(w_vol*inlet_pos - w_inlet/2, -w_tube, 0, el_s, 12)
a.addPoint(w_vol*inlet_pos + w_inlet/2, -w_tube, 0, el_s, 13)
a.addPoint(l_tube/2, -w_tube, 0, el_s, 14)
a.addPoint(l_tube/2, 0, 0, el_s, 15)



a.addPoint(w_vol/2, l_inlet + l_vol, 0, el_s, 19) #ending of the vol
a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet + l_vol, 0, el_s, 20)
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet + l_vol, 0, el_s, 21)
a.addPoint(-w_vol/2, l_inlet + l_vol, 0, el_s, 22)
a.addPoint(-w_vol/2, l_inlet + l_vol*outlet_pos - w_outlet/2, 0, el_s, 24) #outlet definition: beggining reflected on the other side
a.addPoint(-w_vol/2, l_inlet + l_vol*outlet_pos + w_outlet/2, 0, el_s, 23)
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet*pressure_inlet_pos + w_pressure_inlet/2, 0, el_s, 27) #pressure tap reflected
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet*pressure_inlet_pos - w_pressure_inlet/2, 0, el_s, 28)

#other points not neccesary for the contour lines
a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet + l_vol*outlet_pos - w_outlet/2, 0, el_s, 31) #outlet reflection
a.addPoint(w_vol*inlet_pos + w_inlet/2, l_inlet + l_vol*outlet_pos + w_outlet/2, 0, el_s, 32)
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet + l_vol*outlet_pos - w_outlet/2, 0, el_s, 29)
a.addPoint(w_vol*inlet_pos - w_inlet/2, l_inlet + l_vol*outlet_pos + w_outlet/2, 0, el_s, 30)


#LINES

#Contour lines

for i in range(0, 15, 1):
    if i < 2:
        a.addLine((i + 1), (i + 1) + 1, (i + 1))
    elif i == 2:
        a.addLine((i + 1), 6, (i + 1))
    elif i == 3 or i == 4:
        continue
    elif i != 8 and i != 14:
        a.addLine((i + 1), (i + 1) + 1, (i + 1))
    elif i == 8:
        a.addLine(1, (i + 1) + 1, (i + 1))
    elif i == 14:
        a.addLine((i + 1), 2, (i + 1))


for i in range(17, 27, 1):
    a.addLine((i + 1), (i + 1) + 1, (i + 1))


#Other lines
a.addLine(9, 18, 16)
a.addLine(28, 1, 28)
#a.addLine(3, 6, 29)
a.addLine(7, 31, 30)
a.addLine(26, 7, 31)
a.addLine(28, 3, 32)
a.addLine(27, 6, 33)
a.addLine(1, 12, 34)
a.addLine(13, 2, 35)
a.addLine(9, 18, 36)
#a.addLine(14, 17, 37)
a.addLine(26, 29, 38)
a.addLine(31, 9, 39)
a.addLine(32, 18, 40)
a.addLine(32, 20, 41)
a.addLine(23, 30, 42)
a.addLine(24, 29, 43)
a.addLine(30, 21, 44)
a.addLine(29, 31, 45)
a.addLine(30, 32, 46)
a.addLine(29, 30, 47)
a.addLine(31, 32, 48)

#Curve Loops

a.addCurveLoop([1, 2, -32, 28], 1)
a.addCurveLoop([32, 3, -33, 27], 2)
#a.addCurveLoop([3, 4, 5, -29], 3)
a.addCurveLoop([33, 6, -31, 26], 4)
a.addCurveLoop([31, 30, -45, -38], 5)
a.addCurveLoop([25, 38, -43, 24], 6)
a.addCurveLoop([7, 8, -39, -30], 7)
a.addCurveLoop([45, 48, -46, -47], 8)
a.addCurveLoop([39, 16, -40, -48], 9)
a.addCurveLoop([43, 47, -42, 23], 10)
a.addCurveLoop([46, 41, 20, -44], 11)
a.addCurveLoop([40, 18, 19, -41], 12)
a.addCurveLoop([42, 44, 21, 22], 13)
a.addCurveLoop([9, -34, 10, 11], 14)
a.addCurveLoop([12, 35, -1, 34], 15)
a.addCurveLoop([13, 14, 15, -35], 16)

#SURFACES
for i in range(1, 17, 1):
    try:
        a.addPlaneSurface([i], i)
    except:
        print("Error en addPlaneSurface numero", i)
        continue

extrusionlist = []
for i in range(1, 17, 1):
    try:
        extrusionlist.append(a.extrude([(2, i)], 0, 0, extrusion_z, numElements=[1], recombine=True))
    except:
        print("Error en extrude numero", i)
        continue

gmsh.model.geo.synchronize() #without this and not applying it, no points will be created. Put it before transfinite lines.

#TRANSFINITE LINES
#Horizontal Lines

inlet_left_hor = [25, 138, 43, -140, 42, -228, -21, -294]
inlet_center_hor = [1, 12, 32, 33, 31, 45, 46, -20, 50, -52, -74, -96, -118, -184, -250, 336]
#pressure_inlet_hor = [3, -5, -96]
inlet_right_hor = [7, 160, 39, -162, 40, -206, -19, -272]
tube_left = [-314, -9, 11, 316]
tube_right = [13, -15, -360, 358]

w = [inlet_left_hor_type, inlet_center_hor_type, inlet_right_hor_type, tube_left_type, tube_right_type]
x = [inlet_left_hor, inlet_center_hor, inlet_right_hor, tube_left, tube_right]
y = [inlet_left_hor_el, inlet_center_hor_el, inlet_right_hor_el, tube_left_el, tube_right_el]
z = [inlet_left_hor_sp, inlet_center_hor_sp, inlet_right_hor_sp, tube_left_sp, tube_right_sp]


for i in range(len(x)):
   for j in range(len(x[i])):
       gmsh.model.mesh.setTransfiniteCurve((x[i][j]), (y[i]), meshType=(w[i]), coef=(z[i]))

#Vertical Lines

inlet_begin_ver = [-28, -53, 2, 51]
inlet_pressure_ver = [-27, -75, 3, 73]
inlet_end_ver = [-26, -97, 6, 95]
vol_inlet_ver = [-24, -141, 38, -119, 30, 117, 8, 161]
vol_outlet_ver = [-23, -229, 47, -185, 48, 183, 16, 205]
vol_end_ver = [-22, -295, 44, -251, 41, 249, 18, 271]
tube_ver = [-315, 317, 337, 359, -10, -34, 35, 14]

m = [inlet_begin_ver, inlet_pressure_ver, inlet_end_ver, vol_inlet_ver, vol_outlet_ver, vol_end_ver, tube_ver]
n = [inlet_begin_ver_el, inlet_pressure_ver_el, inlet_end_ver_el, vol_inlet_ver_el, vol_outlet_ver_el, vol_end_ver_el, tube_ver_el]
o = [inlet_begin_ver_sp, inlet_pressure_ver_sp, inlet_end_ver_sp, vol_inlet_ver_sp, vol_outlet_ver_sp, vol_end_ver_sp, tube_ver_sp]
p = [inlet_begin_ver_type, inlet_pressure_ver_type, inlet_end_ver_type, vol_inlet_ver_type, vol_outlet_ver_type, vol_end_ver_type, tube_ver_type]

for i in range(len(m)):
    for j in range(len(m[i])):
       gmsh.model.mesh.setTransfiniteCurve((m[i][j]), (n[i]), meshType=(p[i]), coef=(o[i]))

#Transfinite surfaces & volumes

for i in range(1, 17, 1):
    if i != 3:
        gmsh.model.mesh.setTransfiniteSurface(i)
        gmsh.model.mesh.setRecombine(2, i)


for i in range(len(extrusionlist)):
    for j in range(len(extrusionlist[i])):
        if j == 1:
            gmsh.model.mesh.setTransfiniteVolume(extrusionlist[i][j][1])
        elif j != 1:
            gmsh.model.mesh.setTransfiniteSurface(extrusionlist[i][j][1])
            gmsh.model.mesh.setRecombine(2, extrusionlist[i][j][1])

#PHYSICAL GROUPS

frontbacklist = []

for i in range(1, 17, 1):
    if i != 3:
        frontbacklist.append(i)

for i in range(len(extrusionlist)):
        if i != 2:
            frontbacklist.append(extrusionlist[i][0][1])

gmsh.model.addPhysicalGroup(2, frontbacklist, name="frontandBack")

gmsh.model.addPhysicalGroup(2, [325], name="inlet")
gmsh.model.addPhysicalGroup(2, [369], name="outlet")

wallslist = [321, 69, 91, 113, 145, 157, 245, 311, 307, 263, 285, 281, 215, 171, 167, 105, 83, 61, 373, 365, 343, 329]
gmsh.model.addPhysicalGroup(2, wallslist, name="walls")

fluidlist = []

for i in range(len(extrusionlist)):
        if i != 2:
            fluidlist.append(extrusionlist[i][1][1])

gmsh.model.addPhysicalGroup(3, fluidlist, name="fluid")

#MESH GENERATION

gmsh.model.mesh.generate(1)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.generate(3)

from datetime import datetime

gmsh.write("vrfb_dampercube_"+ datetime.now().strftime("%d-%m-%Y_%H-%M-%S") +".msh2")

gmsh.fltk.run() #without this and not applying it, no gmsh window will appear.
gmsh.finalize()