import pytest
from figura.d3 import *
from OCC.Core.gp import (
    gp_Pnt,
    gp_Vec,
    gp_Dir
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


def test_vector():
    vec = Vector(1, 2, 3)
    assert vec.x == 1
    assert vec.y == 2
    assert vec.z == 3
    assert vec.vec().IsEqual(gp_Vec(1, 2, 3), 1e-15, 1e-15)

    s = str(vec)
    assert s == "<class 'figura.d3._geometry.Vector'>(x=1.0, y=2.0, z=3.0)"

    gv = gp_Vec(3, 2, 1)
    v = Vector.from_vec(gv)
    assert v.x == 3
    assert v.y == 2
    assert v.z == 1

    opposite_vec = -vec
    assert opposite_vec.x == -1
    assert opposite_vec.y == -2
    assert opposite_vec.z == -3


def test_direction():
    dir = Direction(1, 2, 3)
    assert dir.x == 0.2672612419124244
    assert dir.y == 0.5345224838248488
    assert dir.z == 0.8017837257372732
    assert dir.dir().IsEqual(gp_Dir(1, 2, 3), 1e-15)

    s = str(dir)
    assert s == "<class 'figura.d3._geometry.Direction'>(x=0.2672612419124244, y=0.5345224838248488, z=0.8017837257372732)"

    opposite_dir = -dir
    assert opposite_dir.x == -0.2672612419124244
    assert opposite_dir.y == -0.5345224838248488
    assert opposite_dir.z == -0.8017837257372732


def test_axis1():
    pt = Point(0, 1, 0)
    dir_x = Direction(1, 0, 0)
    ax1 = Axis1(pt, dir_x)
    assert ax1.location.x == 0
    assert ax1.location.y == 1
    assert ax1.location.z == 0

    assert ax1.direction.x == 1
    assert ax1.direction.y == 0
    assert ax1.direction.z == 0

    assert ax1.ax1().Location().IsEqual(gp_Pnt(0, 1, 0), 1e-15)
    assert ax1.ax1().Direction().IsEqual(gp_Dir(1, 0, 0), 1e-15)


def test_axis1_not_a_point():
    with pytest.raises(TypeError):
        dir_x = Direction(1, 0, 0)
        Axis1("a", dir_x)


def test_axis1_not_a_dir():
    with pytest.raises(TypeError):
        pt = Point(0, 1, 0)
        Axis1(pt, "a")


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

    assert ax2.ax2().Location().IsEqual(gp_Pnt(0, 1, 0), 1e-15)
    assert ax2.ax2().Direction().IsEqual(gp_Dir(1, 0, 0), 1e-15)


def test_axis2_not_a_point():
    with pytest.raises(TypeError):
        dir_x = Direction(1, 0, 0)
        Axis2("a", dir_x)


def test_axis2_not_a_dir():
    with pytest.raises(TypeError):
        pt = Point(0, 1, 0)
        Axis2(pt, "a")
