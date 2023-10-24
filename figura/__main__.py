# Front end for figura

import types
from figura.io import export
from figura._version import __version__


def load_file(file_name):
    with open(file_name) as fp:
        src = "from figura import *\n"
        src += fp.read()
        code = compile(src, file_name, "exec")
    module = types.ModuleType("<script>")
    exec(code, globals(), module.__dict__)

    shps = []
    if hasattr(module, 'export'):
        for obj in module.export:
            shps.append(obj)

    return shps


def save_file(shapes, file_name, file_format='step'):
    export(file_name, shapes, file_format)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog='figura',
        description='Create parametrical 3D models'
    )
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
    parser.add_argument("-v", "--version",
                        version="figura version " + __version__,
                        action="version")
    args = parser.parse_args()

    if args.input:
        shapes = load_file(args.input)
        save_file(shapes, args.output, file_format=args.format)


if __name__ == '__main__':
    main()  # pragma: no cover
