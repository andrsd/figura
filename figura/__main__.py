# Front end for figura
import os
import types
from pathlib import Path
from figura.io import export
from figura._version import __version__


def load_file(file_name):
    with open(file_name) as fp:
        src = "from figura import *\n"
        src += fp.read()
        code = compile(src, file_name, "exec")
    module = types.ModuleType("<script>")
    exec(code, globals(), module.__dict__)

    if hasattr(module, 'export'):
        return module.export
    else:
        raise SystemExit("No shapes were specified for export")


def save_file(shapes, file_name, output_dir, file_format='step'):
    export(os.path.join(output_dir, file_name), shapes, file_format)


def get_file_ext(fmt):
    return "." + fmt


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
        "-o",
        "--output-file",
        help="Output file"
    )
    parser.add_argument(
        "--format",
        choices=['step', 'stl'],
        default='step',
        help="File format: [STEP | STL]"
    )
    parser.add_argument(
        "-O",
        "--output-dir",
        default=os.getcwd(),
        help="Output directory"
    )
    parser.add_argument("-v", "--version",
                        version="figura version " + __version__,
                        action="version")
    args = parser.parse_args()

    if args.input:
        try:
            shapes = load_file(args.input)
            if isinstance(shapes, list):
                if args.output_file is None:
                    args.output_file = Path(Path(args.input).name).with_suffix(
                        get_file_ext(args.format))
                save_file(shapes, args.output_file, args.output_dir,
                          file_format=args.format)
            elif isinstance(shapes, dict):
                for f, shs in shapes.items():
                    out_file = f
                    save_file(shs, out_file, args.output_dir,
                              file_format=args.format)
            else:
                raise SystemExit("I don't know how to export shapes.")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()  # pragma: no cover
