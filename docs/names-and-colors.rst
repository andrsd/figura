Names and Colors
================

With more complicated geometries, it is desired to be able to name individual parts of the model.
This can be achieved via ``name`` property.

.. card:: Naming a shape

   .. code::

      pt1 = Point(0, 0, 0)
      pt2 = Point(1, 0, 0)
      pt3 = Point(0, 1, 0)
      triangle = Face(Polygon([pt1, pt2, pt3]).wire())
      vec = Vector(0, 0, 1)
      solid = triangle.extrude(vec)
      solid.name = 'triangle'

To help users to understand the model, color can be assigned to individual parts of the model.

.. card:: Assign a color

   .. code::

      solid.color = colors.light_blue

The following colors are available in figura:

.. grid:: 3

   .. grid-item-card::

      .. code::

         black
         blue
         red

         medium_blue
         medium_grey
         dark_blue
         light_grey
         light_blue
         orange
         dark_grey
         yellow

         grey1
         grey2
         grey3
         grey4
         grey5
         grey6
         grey7

         gold1
         gold2
         gold3
         gold4
         gold5
         gold6
         gold7

         silver1
         silver2
         silver3
         silver4
         silver5
         silver6
         silver7

   .. grid-item-card::

      .. code::

         red1
         red2
         red3
         red4
         red5
         red6
         red7

         orange1
         orange2
         orange3
         orange4
         orange5
         orange6
         orange7

         yellow1
         yellow2
         yellow3
         yellow4
         yellow5
         yellow6
         yellow7

         green1
         green2
         green3
         green4
         green5
         green6
         green7

   .. grid-item-card::

      .. code::

         teal1
         teal2
         teal3
         teal4
         teal5
         teal6
         teal7

         blue1
         blue2
         blue3
         blue4
         blue5
         blue6
         blue7

         violet1
         violet2
         violet3
         violet4
         violet5
         violet6
         violet7

         purple1
         purple2
         purple3
         purple4
         purple5
         purple6
         purple7
