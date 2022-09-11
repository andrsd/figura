# Front end for figura

from figura import *
import os
import sys
import types
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh


def load_file(file_name):
    with open(file_name) as fp:
        code = compile(fp.read(), file_name, "exec")
    module = types.ModuleType("<script>")
    exec(code, globals(), module.__dict__)

    shps = []
    if hasattr(module, 'export'):
        for obj in module.export:
            shps.append(obj)

    return shps


def save_file(shapes, file_name, file_format='step'):
    fmt = file_format.lower()
    if fmt == 'step':
        step = STEPFile(file_name)
        step.write(shapes)
    elif fmt == 'stl':
        save_file_stl(shapes, file_name, binary=True)
    else:
        raise SystemExit("Unknown format {}.".format(file_format))


def save_file_stl(shapes, file_name, binary=True):
    # meshing params
    linear_deflection = 0.9
    angular_deflection = 0.1

    writer = StlAPI_Writer()
    writer.SetASCIIMode(not binary)
    for idx, shp in enumerate(shapes):
        mesh = BRepMesh_IncrementalMesh(shp.shape(), linear_deflection, False, angular_deflection, True)
        mesh.Perform()
        if not mesh.IsDone():
            raise SystemExit("Mesh is not done.")
        fn = "{}.{}.stl".format(file_name, idx)
        success = writer.Write(shp.shape(), fn)
        if not success:
            raise SystemExit("Failed to write STL file")


def main():
    import OCC.Core.STEPControl as step
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="Input file"
    )
    parser.add_argument(
        "output",
        help="Output file"
    )
    parser.add_argument(
        "--format",
        choices=['step', 'stl'],
        default='step',
        help="File format: [STEP | STL]"
    )
    args = parser.parse_args()

    if args.input:
        shapes = load_file(args.input)
        save_file(shapes, args.output, file_format=args.format)


if __name__ == '__main__':
    main()  # pragma: no cover
