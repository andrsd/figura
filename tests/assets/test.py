from figura import *

model.units = "m"

pt1 = Point(0, 0, 0)
pt2 = Point(1, 1, 1)

edge = Line(pt1, pt2)

#edge2 = Line.from_shape(edge.shape())

# arc = ThreePointArc(pt1, pt2, pt3)
# arc = CenterPointArc(pt1, pt2, pt3)
#
# arc = Arc(pt1=pt1, pt2=pt2, pt3=pt3)
# arc = Arc(center=pt1, pt1=pt2, pt2=pt3)


box = Box(pt1, pt2)
box.name = "box"
box.color = colors.light_blue

#export = [box]
export("box.step", box)
