
from __future__ import print_function

import pprint
pp = pprint.pprint

import pdb
from squeaklib import Point, Rectangle, Form

pp( locals() )

p1 = Point(100,100)
p2 = Point(40,60)
p3 = Point(40,60)

if 0:
    print( p1 > p2 )
    print( p1 >= p2 )
    print( p1 < p2 )
    print( p1 <= p2 )

    print( p3 > p2 )
    print( p3 >= p2 )
    print( p3 < p2 )
    print( p3 <= p2 )


r1 = Rectangle( p1, p2 )
# pdb.set_trace()
r2 = Rectangle.centerExtent(p1, p2)
print(r1)
print(r2)

r3 = Rectangle.leftRightTopBottom( 10, 110, 10, 110 )
print( "r3:"  )
print( r3 )
print( "width: %.2f" % r3.width )
print( "height: %.2f" % r3.height )
print( "area: %.2f" % r3.area )
print( "center: %s" % r3.center )

print( "top: %s" % r3.top )
print( "left: %s" % r3.left )
print( "bottom: %s" % r3.bottom )
print( "right: %s" % r3.right )

print( "bottomcenter: %s" % r3.bottomcenter )
print( "topcenter: %s" % r3.topcenter )
print( "leftcenter: %s" % r3.leftcenter )
print( "rightcenter: %s" % r3.rightcenter )
print( "topleft: %s" % r3.topleft )
print( "topright: %s" % r3.topright )
print( "bottomleft: %s" % r3.bottomleft )
print( "bottomright: %s" % r3.bottomright )


r4 = p1.extent( p2 )
print( "r4:"  )
print( r4 )
print( "width: %.2f" % r4.width )
print( "height: %.2f" % r4.height )
print( "area: %.2f" % r4.area )
print( "center: %s" % r4.center )

print( "top: %s" % r4.top )
print( "left: %s" % r4.left )
print( "bottom: %s" % r4.bottom )
print( "right: %s" % r4.right )

print()
print("p1: %s" % repr(p1))
p2 = p1 * 2
print("p2: %s" % repr(p2))

r5 = p1.extent( p2 )
print("r5 = p1.extent( p2 ) =    %s" % repr(r5))

r6 = p1.corner( p2 )
print("r6 = p1.corner( p2 ) =    %s" % repr(r6))

r7 = p2.rect( p1 )
print("r7 = p2.rect( p1 ) =    %s" % repr(r7))

print()
r8 = Rectangle.centerExtent( Point( 50,50 ), Point(60,60) )
print("r8 = Rectangle.centerExtent( Point( 50,50 ), Point(60,60) ) =    %s" % repr(r8))

print()
r9 = Rectangle.leftRightTopBottom( 10,490,10,890 )
print("r9 = Rectangle.leftRightTopBottom( 10,90,10,90 ) =    %s" % repr(r9))

print()
r10 = Rectangle.merging( (r1,r2,r3,r4,r5,r6,r7,r8,r9) )
print("r10 = Rectangle.merging( (r1,r2,r3,r4,r5,r6,r7,r8,r9) ) =    %s" % repr(r10))


