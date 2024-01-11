import os
import sys
import pytest
from figura.__main__ import load_file, save_file, main
from figura.__init__ import model

assets_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "assets"
)


def test_step(tmp_path):
    file = os.path.join(assets_dir, "box.figura")
    shapes = load_file(file)
    save_file(shapes, "out.step", tmp_path, file_format='STEP')


def test_stl(tmp_path):
    file = os.path.join(assets_dir, "box.figura")
    shapes = load_file(file)
    save_file(shapes, "out", tmp_path, file_format='STL')


def test_wrong_unit():
    with pytest.raises(ValueError):
        model.units = "asdf"


def test_multiple_files(tmp_path):
    file = os.path.join(assets_dir, "2boxes.figura")
    sys.argv = ["figura", file, "-O", str(tmp_path)]
    main()


def test_functions(tmp_path):
    file = os.path.join(assets_dir, "funcs.figura")
    sys.argv = ["figura", file, "-O", str(tmp_path)]
    main()


def test_empty_script(tmp_path):
    file = os.path.join(assets_dir, "empty.figura")
    sys.argv = ["figura", file, "-O", str(tmp_path)]
    with pytest.raises(SystemExit):
        main()


def test_empty_export(tmp_path):
    file = os.path.join(assets_dir, "empty_export.figura")
    sys.argv = ["figura", file, "-O", str(tmp_path)]
    with pytest.raises(SystemExit):
        main()
