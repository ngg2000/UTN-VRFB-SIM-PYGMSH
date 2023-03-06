import gmsh
import sys

#magic

gmsh.initialize()

gmsh.model.add('cubes')

#INPUTS

l = 10
h = 10
d = 7

ncellsl = 5
ncellsh = 10
ncellsextrude = 10



#2D points

downleftpoint = gmsh.model.geo.addPoint(0, 0, 0)
downcenterpoint = gmsh.model.geo.addPoint(l/2, 0, 0)
downrightpoint = gmsh.model.geo.addPoint(l, 0, 0)
upleftpoint = gmsh.model.geo.addPoint(0, h, 0)
upcenterpoint = gmsh.model.geo.addPoint(l/2, h, 0)
uprightpoint = gmsh.model.geo.addPoint(l, h, 0)

#2D lines

downleftline = gmsh.model.geo.addLine(downleftpoint, downcenterpoint)
downrightline = gmsh.model.geo.addLine(downcenterpoint, downrightpoint)
downupleftline = gmsh.model.geo.addLine(downleftpoint, upleftpoint)
upleftline = gmsh.model.geo.addLine(upleftpoint, upcenterpoint)
uprightline = gmsh.model.geo.addLine(upcenterpoint, uprightpoint)
downupcenterline = gmsh.model.geo.addLine(downcenterpoint, upcenterpoint)
downuprightline = gmsh.model.geo.addLine(downrightpoint, uprightpoint)

#2D loops and surfaces

leftloop = gmsh.model.geo.addCurveLoop([downleftline, downupcenterline, -upleftline, -downupleftline])
rightloop = gmsh.model.geo.addCurveLoop([downrightline, downuprightline, -uprightline, -downupcenterline])

leftsurf = gmsh.model.geo.addPlaneSurface([leftloop])
rightsurf = gmsh.model.geo.addPlaneSurface([rightloop])

#2D to 3D extrusions

leftvol = gmsh.model.geo.extrude([(2, leftsurf)], 0, 0, h, recombine=True)
rightvol = gmsh.model.geo.extrude([(2, rightsurf)], 0, 0, h, recombine=True)

gmsh.model.geo.synchronize()

print("Que onda, esta es la info del leftvol: \n", leftvol)

print("Primer ID: superficie opuesta. Por eso arranca con un 2")
print("Segundo ID: volumen, arranca con un 3.")
print("Tercer, cuarto, quinto y sexto ID: Arranca el recorrido del loop con los ID de las superficies extrudadas \n a partir de las lineas (conforme orden en el loop)")

print("Que onda, esta es la info del rightvol: \n", rightvol)

print("propiedades del contorno: ", gmsh.model.getBoundary(dimTags=[(2, rightvol[0][1])], oriented=True))
print("propiedades del contorno: ", gmsh.model.getBoundary(dimTags=[(2, leftvol[0][1])], oriented=True))

#Physical groups ID

gmsh.model.addPhysicalGroup(2, [leftvol[5][1]], name="faceInlet") 
#quinto par, elemento 1 (python arranca en cero, asi que es el 2do) del leftvol
#ojo: es el quinto par que cumple con la condicion de tener dimension 2
#porque fijate que si vas a recorrer la lista, seria el sexto par, no el quinto
#pero te salteas el par con el id del volumen, entonces quedan cinco pares y este es el quinto.
#Tambien destacar que el orden del loop de superficies es el mismo del curve loop.
gmsh.model.addPhysicalGroup(2, [rightvol[3][1]], name="faceOutlet")
#gmsh.model.addPhysicalGroup(2, [])
gmsh.model.addPhysicalGroup(2, [leftvol[4][1],rightvol[4][1]],name="faceTop")
gmsh.model.addPhysicalGroup(2, [leftvol[2][1],rightvol[2][1]],name="faceBottom")
gmsh.model.addPhysicalGroup(2, [leftsurf,rightsurf,leftvol[0][1],rightvol[0][1]],name="faceFrontAndBack")
gmsh.model.addPhysicalGroup(3, [leftvol[1][1],rightvol[1][1]],name="fluid")


#Transfinite curves

gmsh.model.mesh.setTransfiniteCurve(downleftline, ncellsl+1, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(upleftline, ncellsl+1, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(downrightline, ncellsl+1, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(uprightline, ncellsl+1, meshType="Progression", coef=0.80)

gmsh.model.mesh.setTransfiniteCurve(downupleftline, ncellsh+1, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(downuprightline, ncellsh+1, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(downupcenterline, ncellsh+1, meshType="Progression", coef=0.80)

#Transfinite curves with getBoundary

lineone = gmsh.model.getBoundary(dimTags=[(2, leftvol[4][1])], oriented=True)[2][1]
linetwo = gmsh.model.getBoundary(dimTags=[(2, leftvol[4][1])], oriented=True)[3][1]

linefour = gmsh.model.getBoundary(dimTags=[(2, rightvol[4][1])], oriented=True)[3][1]
lineone1 = gmsh.model.getBoundary(dimTags=[(2, leftvol[2][1])], oriented=True)[2][1]
linetwo1 = gmsh.model.getBoundary(dimTags=[(2, leftvol[2][1])], oriented=True)[3][1]

linefour1 = gmsh.model.getBoundary(dimTags=[(2, rightvol[2][1])], oriented=True)[3][1]

linezero1 = gmsh.model.getBoundary(dimTags=[(2, leftvol[0][1])], oriented=True)[1][1]
linezero2 = gmsh.model.getBoundary(dimTags=[(2, leftvol[0][1])], oriented=True)[3][1]

linezero3 = gmsh.model.getBoundary(dimTags=[(2, rightvol[0][1])], oriented=True)[2][1]
linezero4 = gmsh.model.getBoundary(dimTags=[(2, leftvol[0][1])], oriented=True)[2][1]
linezero5 = gmsh.model.getBoundary(dimTags=[(2, leftvol[0][1])], oriented=True)[0][1]

linezero6 = gmsh.model.getBoundary(dimTags=[(2, rightvol[0][1])], oriented=True)[1][1]
linezero7 = gmsh.model.getBoundary(dimTags=[(2, rightvol[0][1])], oriented=True)[3][1]

print("lineone = ", lineone)

gmsh.model.mesh.setTransfiniteCurve(abs(lineone), 11, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linetwo), 11, meshType="Progression", coef=0.80)

gmsh.model.mesh.setTransfiniteCurve(abs(linefour), 11, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(lineone1), 11, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linetwo1), 11, meshType="Progression", coef=0.80)

gmsh.model.mesh.setTransfiniteCurve(abs(linefour1), 11, meshType="Progression", coef=0.80)


gmsh.model.mesh.setTransfiniteCurve(abs(linezero1), 11, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linezero2), 11, meshType="Progression", coef=-0.80)

gmsh.model.mesh.setTransfiniteCurve(abs(linezero3), 11, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linezero4), 6, meshType="Progression", coef=-0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linezero5), 6, meshType="Progression", coef=0.80)

gmsh.model.mesh.setTransfiniteCurve(abs(linezero6), 6, meshType="Progression", coef=0.80)
gmsh.model.mesh.setTransfiniteCurve(abs(linezero7), 6, meshType="Progression", coef=-0.80)

#Transfinite surfaces

gmsh.model.mesh.setTransfiniteSurface(leftsurf)
gmsh.model.mesh.setTransfiniteSurface(rightsurf)
gmsh.model.mesh.setTransfiniteSurface(leftvol[4][1])
gmsh.model.mesh.setTransfiniteSurface(rightvol[4][1])
gmsh.model.mesh.setTransfiniteSurface(leftvol[2][1])
gmsh.model.mesh.setTransfiniteSurface(rightvol[2][1])
gmsh.model.mesh.setTransfiniteSurface(leftvol[3][1])
gmsh.model.mesh.setTransfiniteSurface(rightvol[3][1])
gmsh.model.mesh.setTransfiniteSurface(leftvol[5][1])
gmsh.model.mesh.setTransfiniteSurface(rightvol[5][1])
gmsh.model.mesh.setTransfiniteSurface(leftvol[0][1])
gmsh.model.mesh.setTransfiniteSurface(rightvol[0][1])
gmsh.model.mesh.setTransfiniteVolume(1)
gmsh.model.mesh.setTransfiniteVolume(2)


print(gmsh.model.getBoundary(dimTags=[(2, rightvol[2][1])], oriented=True))

gmsh.model.mesh.setRecombine(2, leftsurf)
gmsh.model.mesh.setRecombine(2, rightsurf)
gmsh.model.mesh.setRecombine(2, leftvol[4][1])
gmsh.model.mesh.setRecombine(2, rightvol[4][1])
gmsh.model.mesh.setRecombine(2, leftvol[2][1])
gmsh.model.mesh.setRecombine(2, rightvol[2][1])
gmsh.model.mesh.setRecombine(2, leftvol[3][1])
gmsh.model.mesh.setRecombine(2, rightvol[3][1])
gmsh.model.mesh.setRecombine(2, leftvol[5][1])
gmsh.model.mesh.setRecombine(2, rightvol[5][1])
gmsh.model.mesh.setRecombine(2, leftvol[0][1])
gmsh.model.mesh.setRecombine(2, rightvol[0][1])

gmsh.model.mesh.generate(1)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.generate(3)

gmsh.write("cubos_20230223.msh")

gmsh.fltk.run()
gmsh.finalize()

