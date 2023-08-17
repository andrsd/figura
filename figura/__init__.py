from .geometry import (Direction, Vector, Axis1, Axis2, Plane, Geometry)
from .shapes import (Shape, Point, Edge, Wire, Face, Shell, Solid, Polygon, Line, ArcOfCircle, Circle, Spline)
from .primitives import (Box, Cylinder, Sphere, Prism)
from .io import (STEPFile, STLFile, export)
from .model import (Model)
from .colormap import (ColorMap)
from ._version import (__version__)

model = Model()
colors = ColorMap()

__all__ = [
    'Geometry',
    'Direction',
    'Vector',
    'Axis1',
    'Axis2',
    'Plane',
    'Shape',
    'Point',
    'Edge',
    'Wire',
    'Polygon',
    'Spline',
    'Face',
    'Shell',
    'Solid',
    'Box',
    'Cylinder',
    'Sphere',
    'Prism',
    'Line',
    'ArcOfCircle',
    'Circle',
    'STEPFile',
    'STLFile',
    'model',
    'colors',
    'export'
]
