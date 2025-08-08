"""Example: Doublet Lens Commands System"""

import numpy as np
import KrakenOS as Kos

# _________________________________________#

P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 0.1
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0

# _________________________________________#

P_Obj2 = Kos.surf()
P_Obj2.Rc = 0.0
P_Obj2.Thickness = 10
P_Obj2.Glass = "AIR"
P_Obj2.Diameter = 30.0

# _________________________________________#

L1a = Kos.surf()
L1a.Rc = 9.284706570002484e001
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0
L1a.Axicon = 0

# _________________________________________#

L1b = Kos.surf()
L1b.Rc = -3.071608670000159e001
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30

# _________________________________________#

L1c = Kos.surf()
L1c.Rc = -7.819730726078505e001
L1c.Thickness = 9.737604742910693e001
L1c.Glass = "AIR"
L1c.Diameter = 30

# _________________________________________#

P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 18.0
P_Ima.Name = "Plano imagen"

# _________________________________________#

A = [P_Obj, P_Obj2, L1a, L1b, L1c, P_Ima]
configuracion_1 = Kos.Setup()

# _________________________________________#

Doublet = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Doublet)

# _________________________________________#

pSource_0 = [0, 14, 0]
tet = 0.1
dCos = [0.0, np.sin(np.deg2rad(tet)), -np.cos(np.deg2rad(tet))]
W = 0.4
Doublet.Trace(pSource_0, dCos, W)
Rayos.push()

# _________________________________________#

Kos.display3d(Doublet, Rayos, 2)

# _________________________________________#

print("Distancia focal efectiva")
print(Doublet.EFFL)
print("Plano principal anterior")
print(Doublet.PPA)
print("Plano principal posterior")
print(Doublet.PPP)
print("Superficies tocadas por el rayo")
print(Doublet.SURFACE)
print("Nombre de la superficie")
print(Doublet.NAME)
print("Vidrio de la superficie")
print(Doublet.GLASS)
print("Coordenadas del rayo en las superficies")
print(Doublet.XYZ)
print("Etc, ver documentaciòn")
print(Doublet.S_XYZ)
print(Doublet.T_XYZ)
print(Doublet.OST_XYZ)
print(Doublet.DISTANCE)
print(Doublet.OP)
print(Doublet.TOP)
print(Doublet.TOP_S)
print(Doublet.ALPHA)
print(Doublet.S_LMN)
print(Doublet.LMN)
print(Doublet.R_LMN)
print(Doublet.N0)
print(Doublet.N1)
print(Doublet.WAV)
print(Doublet.G_LMN)
print(Doublet.ORDER)
print(Doublet.GRATING)
print(Doublet.RP)
print(Doublet.RS)
print(Doublet.TP)
print(Doublet.TS)
print(Doublet.TTBE)
print(Doublet.TT)
print(Doublet.BULK_TRANS)
