import pytest
from figura.geometry import (
    Point,
    Vector,
    Direction,
    Axis2,
    Geometry
)
from OCC.Core.gp import (
    gp_Pnt,
    gp_Vec,
    gp_Dir
)
import os


assets_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "assets"
)


def test_point():
    pt = Point(1, 2, 3)
    assert pt.x == 1
    assert pt.y == 2
    assert pt.z == 3
    assert pt.obj().IsEqual(gp_Pnt(1, 2, 3), 1e-15)


def test_vector():
    vec = Vector(1, 2, 3)
    assert vec.x == 1
    assert vec.y == 2
    assert vec.z == 3
    assert vec.obj().IsEqual(gp_Vec(1, 2, 3), 1e-15, 1e-15)


def test_direction():
    dir = Direction(1, 2, 3)
    assert dir.x == 0.2672612419124244
    assert dir.y == 0.5345224838248488
    assert dir.z == 0.8017837257372732
    assert dir.obj().IsEqual(gp_Dir(1, 2, 3), 1e-15)


def test_axis2():
    pt = Point(0, 1, 0)
    dir_x = Direction(1, 0, 0)
    ax2 = Axis2(pt, dir_x)
    assert ax2.location.x == 0
    assert ax2.location.y == 1
    assert ax2.location.z == 0

    assert ax2.direction.x == 1
    assert ax2.direction.y == 0
    assert ax2.direction.z == 0

    assert ax2.obj().Location().IsEqual(gp_Pnt(0, 1, 0), 1e-15)
    assert ax2.obj().Direction().IsEqual(gp_Dir(1, 0, 0), 1e-15)


def test_axis2_not_a_point():
    with pytest.raises(TypeError):
        dir_x = Direction(1, 0, 0)
        Axis2("a", dir_x)


def test_axis2_not_a_dir():
    with pytest.raises(TypeError):
        pt = Point(0, 1, 0)
        Axis2(pt, "a")


def test_read_step():
    geo = Geometry()
    geo.read(os.path.join(assets_dir, "cube.step"))


def test_read_non_existent_step():
    geo = Geometry()
    with pytest.raises(SystemExit):
        geo.read(os.path.join(assets_dir, "non-existent.step"))


def test_read_unknown():
    geo = Geometry()
    with pytest.raises(SystemError):
        geo.read(os.path.join(assets_dir, "cube.step"), format="ASDF")
