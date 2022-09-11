# Front end for figura

from figura import *
import os
import sys
import types


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
        stl = STLFile(file_name)
        stl.write(shapes)
    else:
        raise SystemExit("Unknown format {}.".format(file_format))


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
