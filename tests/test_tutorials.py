import os
from figura.__main__ import load_file

tuts_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../tutorials"
)


def test_bottle():
    file = os.path.join(tuts_dir, "bottle/bottle.figura")
    load_file(file)


def test_2d_geometry():
    file = os.path.join(tuts_dir, "2d-geometry/channel.figura")
    load_file(file)
