import pytest
import math
from figura.d2 import *
from OCC.Core.gp import (
    gp_Pnt2d,
    gp_Vec2d,
    gp_Dir2d
)


def test_origin_x_2d():
    ox = Geometry.OX()
    assert ox.location.x == 0
    assert ox.location.y == 0

    assert ox.direction.x == 1
    assert ox.direction.y == 0


def test_origin_y_2d():
    oy = Geometry.OY()
    assert oy.location.x == 0
    assert oy.location.y == 0

    assert oy.direction.x == 0
    assert oy.direction.y == 1


def test_direction_x_2d():
    dx = Geometry.DX()
    assert dx.x == 1
    assert dx.y == 0


def test_direction_y_2d():
    dy = Geometry.DY()
    assert dy.x == 0
    assert dy.y == 1


def test_vector_2d():
    vec = Vector(1, 2)
    assert vec.x == 1
    assert vec.y == 2
    assert vec.vec().IsEqual(gp_Vec2d(1, 2), 1e-15, 1e-15)

    s = str(vec)
    assert s == "<class 'figura.d2._geometry.Vector'>(x=1.0, y=2.0)"

    gv = gp_Vec2d(3, 2)
    v = Vector.from_vec(gv)
    assert v.x == 3
    assert v.y == 2

    opposite_vec = -vec
    assert opposite_vec.x == -1
    assert opposite_vec.y == -2


def test_direction():
    dir = Direction(1, 2)
    assert math.isclose(dir.x, 0.447213595499958, abs_tol=1e-15)
    assert math.isclose(dir.y, 0.8944271909999159, abs_tol=1e-15)
    assert dir.dir().IsEqual(gp_Dir2d(1, 2), 1e-15)

    s = str(dir)
    assert s == "<class 'figura.d2._geometry.Direction'>(x=0.4472135954999579, y=0.8944271909999159)"

    opposite_dir = -dir
    assert math.isclose(opposite_dir.x, -0.447213595499958, abs_tol=1e-15)
    assert math.isclose(opposite_dir.y, -0.894427190999916, abs_tol=1e-15)


def test_axis_2d():
    pt = Point(0, 1)
    dir_x = Direction(1, 0)
    ax1 = Axis(pt, dir_x)
    assert ax1.location.x == 0
    assert ax1.location.y == 1

    assert ax1.direction.x == 1
    assert ax1.direction.y == 0

    assert ax1.ax().Location().IsEqual(gp_Pnt2d(0, 1), 1e-15)
    assert ax1.ax().Direction().IsEqual(gp_Dir2d(1, 0), 1e-15)


def test_axis1_not_a_point_2d():
    with pytest.raises(TypeError):
        dir_x = Direction(1, 0)
        Axis("a", dir_x)


def test_axis1_not_a_dir():
    with pytest.raises(TypeError):
        pt = Point(0, 1)
        Axis(pt, "a")


def test_axis2_2d():
    pt = Point(0, 1)
    dir_x = Direction(1, 0)
    ax2 = Axis2(pt, dir_x)
    assert ax2.location.x == 0
    assert ax2.location.y == 1

    assert ax2.direction.x == 1
    assert ax2.direction.y == 0

    assert ax2.ax2().Location().IsEqual(gp_Pnt2d(0, 1), 1e-15)
    assert ax2.ax2().XDirection().IsEqual(gp_Dir2d(1, 0), 1e-15)
    assert ax2.ax2().YDirection().IsEqual(gp_Dir2d(0, 1), 1e-15)


def test_axis2_not_a_point_2d():
    with pytest.raises(TypeError):
        dir_x = Direction(1, 0)
        Axis2("a", dir_x)


def test_axis2_not_a_dir_2d():
    with pytest.raises(TypeError):
        pt = Point(0, 1)
        Axis2(pt, "a")
