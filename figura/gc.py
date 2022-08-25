from OCC.Core.GC import (
    GC_MakeArcOfCircle,
    GC_MakeSegment
)


class GeoGeometry(object):

    def __init__(self):
        pass


class GeoCurve(GeoGeometry):

    def __init__(self):
        pass


class Segment(GeoCurve):

    def __init__(self, pt1, pt2):
        super().__init__()
        mk = GC_MakeSegment(pt1.obj(), pt2.obj())
        if not mk.IsDone():
            raise SystemExit("Segment was not created")
        self._segment = mk.Value()

    def obj(self):
        return self._segment


class ArcOfCircle(GeoCurve):

    def __init__(self, pt1, pt2, pt3):
        super().__init__()
        mk = GC_MakeArcOfCircle(pt1.obj(), pt2.obj(), pt3.obj())
        if not mk.IsDone():
            raise SystemExit("ArcOfCircle was not created")
        self._arc = mk.Value()

    def obj(self):
        return self._arc
