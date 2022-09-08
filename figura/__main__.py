# Front end for figura

from figura import *
import os
import sys
import types
import OCC.Core.STEPControl as step


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


def save_file(shapes, file_name):
    step_writer = step.STEPControl_Writer()
    for shp in shapes:
        step_writer.Transfer(shp.shape(), step.STEPControl_AsIs)
    step_writer.Write(file_name)


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
    args = parser.parse_args()

    if args.input:
        shapes = load_file(args.input)
        save_file(shapes, args.output)


if __name__ == '__main__':
    main()  # pragma: no cover
