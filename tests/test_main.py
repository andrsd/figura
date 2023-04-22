import os
import pytest
from figura.__main__ import load_file, save_file
from figura.__init__ import model

assets_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "assets"
)


def test_step():
    file = os.path.join(assets_dir, "box.figura")
    shapes = load_file(file)
    save_file(shapes, "out.step", file_format='STEP')


def test_stl():
    file = os.path.join(assets_dir, "box.figura")
    shapes = load_file(file)
    save_file(shapes, "out", file_format='STL')


def test_wrong_unit():
    with pytest.raises(ValueError):
        model.units = "asdf"
