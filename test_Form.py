
from squeaklib import Point, Rectangle, Form


d = Form.dotOfSize(511)
d.img.save("Form.dotOfSize(511).png")

p1 = Point(100,100)
p2 = Point(40,60)
p3 = Point(40,60)


r1 = Rectangle( p1, p2 )
print("R1: %s" % repr(r1) )
r2 = Rectangle.centerExtent(p1, p2)
imageRectangles( [r1,r2] )

r3 = Rectangle.leftRightTopBottom( 10, 110, 10, 110 )
imageRectangles( [r1,r2,r3] )

r4 = p1.extent( p2 )
imageRectangles( [r1,r2,r3,r4] )

p2 = p1 * 2
imageRectangles( [r1,r2,r3,r4] )

r5 = p1.extent( p2 )
imageRectangles( [r1,r2,r5] )

r6 = p1.corner( p2 )
imageRectangles( [r1,r2,r6] )

r7 = p2.rect( p1 )
imageRectangles( [r1,r2,r7] )

r8 = Rectangle.centerExtent( Point( 50,50 ), Point(60,60) )
print("r8 = Rectangle.centerExtent( Point( 50,50 ), Point(60,60) ) =    %s" % repr(r8))

print()
r9 = Rectangle.leftRightTopBottom( 10,490,10,890 )
print("r9 = Rectangle.leftRightTopBottom( 10,90,10,90 ) =    %s" % repr(r9))

print()
r10 = Rectangle.merging( (r1,r2,r3,r4,r5,r6,r7,r8,r9) )
print("r10 = Rectangle.merging( (r1,r2,r3,r4,r5,r6,r7,r8,r9) ) =    %s" % repr(r10))

imageRectangles( [r1,r2,r3,r4,r5,r6,r7,r8,r9] )

pp([r1,r2,r3,r4,r5,r6,r7,r8,r9])

