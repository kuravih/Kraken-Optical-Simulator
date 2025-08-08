"""Example: Diffraction Grating Reflection"""

import numpy as np
import KrakenOS as Kos

# _________________________________________#

P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 250
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


# _________________________________________#

Dif_Obj = Kos.surf()
Dif_Obj.Rc = 0.0
Dif_Obj.Thickness = -250
Dif_Obj.Glass = "MIRROR"
Dif_Obj.Diameter = 30.0
Dif_Obj.Grating_D = 1000 / 600
Dif_Obj.Diff_Ord = 1
Dif_Obj.Grating_Angle = 0.0


# _________________________________________#

P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Name = "Plano imagen"
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 1000.0
P_Ima.Drawing = 0

# _________________________________________#

A = [P_Obj, Dif_Obj, P_Ima]
configuracion_1 = Kos.Setup()

# _________________________________________#

Doublet = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Doublet)

# _________________________________________#

pSource_0 = [0, 0, 0.0]
tet = 0
dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
w = np.linspace(0.35, 0.90, 10)
for W in w:
    Doublet.Trace(pSource_0, dCos, W)
    print(Doublet.XYZ[-1])
    Rayos.push()


# ______________________________________#

Kos.display3d(Doublet, Rayos, 1)
