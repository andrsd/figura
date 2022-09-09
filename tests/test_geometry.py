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


def test_origin_x():
    ox = Geometry.OX()
    assert ox.location.x == 0
    assert ox.location.y == 0
    assert ox.location.z == 0

    assert ox.direction.x == 1
    assert ox.direction.y == 0
    assert ox.direction.z == 0


def test_origin_y():
    oy = Geometry.OY()
    assert oy.location.x == 0
    assert oy.location.y == 0
    assert oy.location.z == 0

    assert oy.direction.x == 0
    assert oy.direction.y == 1
    assert oy.direction.z == 0


def test_origin_z():
    oz = Geometry.OZ()
    assert oz.location.x == 0
    assert oz.location.y == 0
    assert oz.location.z == 0

    assert oz.direction.x == 0
    assert oz.direction.y == 0
    assert oz.direction.z == 1


def test_direction_x():
    dx = Geometry.DX()
    assert dx.x == 1
    assert dx.y == 0
    assert dx.z == 0


def test_direction_y():
    dy = Geometry.DY()
    assert dy.x == 0
    assert dy.y == 1
    assert dy.z == 0


def test_direction_z():
    dz = Geometry.DZ()
    assert dz.x == 0
    assert dz.y == 0
    assert dz.z == 1


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
