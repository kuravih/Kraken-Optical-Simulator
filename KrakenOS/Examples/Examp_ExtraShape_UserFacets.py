"""
Example: Faceted Optical Surface Using KrakenOS

This script defines an optical system using KrakenOS, in which one of the surfaces
is composed of planar facets. Each facet has its own normal vector, introducing
small tilts over the surface. The surface is constructed over a square area and
tested using ray tracing.

Units: All spatial dimensions are in millimeters (mm).

Author: Joel H. V.
Date:12/04/25
"""

import numpy as np
import KrakenOS as Kos

# --- Define the entrance pupil surface ---
P_Obj = Kos.surf()
P_Obj.Rc = 0.0  # Radius of curvature (flat)
P_Obj.Thickness = 10  # Distance to next surface (mm)
P_Obj.Glass = "AIR"  # Medium is air
P_Obj.Diameter = 30.0  # Diameter in mm

# --- Define a square aperture rotated 45 degrees ---
radius = 15  # Half-width of the square (mm)
angle = 45  # Rotation angle (degrees)
px = [radius * np.cos(np.radians(angle + d)) for d in [0, 90, 180, 270, 0]]
py = [radius * np.sin(np.radians(angle + d)) for d in [0, 90, 180, 270, 0]]

# --- Define a flat BK7 surface with the above UDA (Useful Diameter Area) ---
L1a = Kos.surf()
L1a.Rc = 0.0
L1a.Thickness = 9.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0
L1a.UDA = [px, py]

# -----------------------------------------------------------------------------
# Function to generate facet centers and normals for a faceted surface


def generate_facets(_n, _m, deviation=0.1):
    """
    Generates centers and normal vectors for a square grid of n x n planar facets.

    Parameters:
    - n: Number of facets per side (int)
    - m: Total width of the square surface (float, in mm)
    - deviation: Max angular deviation from the Z-axis (float, in radians)

    Returns:
    - X0, Y0: Arrays (n x n) of facet center coordinates in x and y
    - NX, NY, NZ: Arrays (n x n) of the unit normal vector components
    """
    step = _m / _n
    x = np.linspace(-_m / 2 + step / 2, _m / 2 - step / 2, _n)
    y = np.linspace(-_m / 2 + step / 2, _m / 2 - step / 2, _n)
    x0, y0 = np.meshgrid(x, y)

    ang_x = np.random.uniform(-deviation, deviation, size=(_n, _n))
    ang_y = np.random.uniform(-deviation, deviation, size=(_n, _n))

    nx = np.sin(ang_x)  # x-component of normal
    ny = np.sin(ang_y)  # y-component of normal
    nz = np.sqrt(1.0 - nx**2 - ny**2)  # z-component of unit normal

    return x0, y0, nx, ny, nz


# -----------------------------------------------------------------------------
# Define a callable class to represent the faceted surface


class FacetedSurface:
    def __init__(self, _x0, _y0, _nx, _ny, _nz, _m):
        """
        Initialize the surface object.

        Parameters:
        - X0, Y0: Grids of facet center coordinates
        - NX, NY, NZ: Grids of facet normal components
        - m: Total width of the surface in mm
        """
        self.x0 = _x0
        self.y0 = _y0
        self.nx = _nx
        self.ny = _ny
        self.nz = _nz
        self.m = _m
        self.n = _x0.shape[0]

    def __call__(self, x, y, E=None):
        """
        Evaluate the height z of the surface at coordinates x, y.
        This method is compatible with KrakenOS's ExtraData surface interface.

        Parameters:
        - x, y: Arrays or scalars of spatial coordinates (mm)
        - E: Unused (placeholder for KrakenOS compatibility)

        Returns:
        - z: Array of heights corresponding to each (x, y) in mm
        """
        step = self.m / self.n
        x = np.asarray(x)
        y = np.asarray(y)

        j = np.clip(np.floor((x + self.m / 2) / step).astype(int), 0, self.n - 1)
        i = np.clip(np.floor((y + self.m / 2) / step).astype(int), 0, self.n - 1)

        x0 = self.x0[i, j]
        y0 = self.y0[i, j]
        nx = self.nx[i, j]
        ny = self.ny[i, j]
        nz = self.nz[i, j]

        numerator = nx * (x - x0) + ny * (y - y0)
        z = -numerator / nz
        return z


# -----------------------------------------------------------------------------
# Create an instance of the faceted surface and assign it to a KrakenOS surface

n = 10  # Number of facets per side
m = 30.0  # Width of the surface (mm)
X0, Y0, NX, NY, NZ = generate_facets(n, m, deviation=0.4)
Faceted = FacetedSurface(X0, Y0, NX, NY, NZ, m)

L1c = Kos.surf()
L1c.Thickness = 300.0
L1c.Diameter = m
L1c.ExtraData = [Faceted, None]  # Second argument is unused
L1c.Glass = "AIR"
L1c.UDA = [px, py]  # Use the same UDA as L1a
L1c.DerPres = 0.000  # cero by default
L1c.Res = 1  # One by default

# -----------------------------------------------------------------------------
# Define the image plane

P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 300.0
P_Ima.Name = "Image plane"

# -----------------------------------------------------------------------------
# Assemble optical system and perform ray tracing

surfaces = [P_Obj, L1a, L1c, P_Ima]
Config_1 = Kos.Setup()
Lens = Kos.system(surfaces, Config_1)
Rays = Kos.raykeeper(Lens)

Wav = 0.45  # Wavelength in microns


# Rays from center of each facet (correctly using i, j order)

for _i in range(n):
    for _j in range(n):
        pSource = [X0[_i, _j], Y0[_i, _j], 0.0]
        dCos = [0.0, 0.0, 1.0]
        Lens.Trace(pSource, dCos, Wav)
        Rays.push()

# ----------------------------------------------------------------------------
# Visualization

Kos.display3d(Lens, Rays, 0)
Kos.display2d(Lens, Rays, 0)
