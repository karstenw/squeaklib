

__ALL__ = ('makePoint', 'imageRectangles',
           'Point', 'Rectangle',
           'Form', 'Region')

import math
import random
import pprint
pp = pprint.pprint

import PIL
import PIL.Image
import PIL.ImageDraw as ImageDraw

import pdb
kwdbg = True

import photobot as pb


# last py2 remnants...
try:
    long
except NameError:
    long = int


def sign( number ):
    """I can't believe that Python does not have a sign() function."""

    if number > 0:
        return +1
    elif number < 0:
        return -1
    return 0


def makePoint( *args  ):
    "Tries to create a Point from args."
    n = len(args)
    
    if kwdbg and 0:
        print("makePoint( %s )" % (str(args),) )
    
    if n == 1:
        typ = type( args[0] )
        if typ in (Point,):
            return args[0]
        elif typ in (long, int, float):
            return Point( args[0], args[0] )
        elif typ in (list, tuple):
            return Point( args[0][0], args[0][1] )
    elif n == 2:
        return Point( args[0], args[1] )
    return None

def imageRectangles( reclist, exportname="imageRectangles()_", frame=(10,10) ):
    # pdb.set_trace()
    frame = makePoint( frame )
    rectangles = []
    scale = 4.0
    points = []
    for r in reclist:
        rs = r * scale
        rectangles.append( rs )
        points.extend( rs.asPointList() )
        
    minPoint = min( points )
    maxPoint = max( points )
    
    w = maxPoint.x - minPoint.x
    w = w + 2 * frame.x
    h = maxPoint.y - minPoint.y
    h = h + 2 * frame.y
    f = Form(w,h)
    f.canvas.fill( (0,0,0, 0) )
    draw = PIL.ImageDraw.Draw(f.canvas.top.img)

    for i,r in enumerate(rectangles):
        x1,y1,x2,y2 = r.asArray()
        w, h = int(r.width), int(r.height)
        # f.canvas.fill( (15, 15, 90, 31), x1, y1, w, h )
        c1 = int( 127*random.random() )
        c2 = int( 31+127*random.random() )
        draw.rectangle( (x1,y1, w,h), fill=(c1, c2, 127,15),
                         outline=(0,0,0,127), width=1)
    f.canvas.export(exportname + pb.datestring(), unique=True  )

class Point(object):
    "Translated from a Squeak 3.7 image"
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __repr__( self ):
        # return u"Point( %.2f, %.2f )" % (float(self.x), float(self.y) )
        return u"Point( %s, %s )" % (str(self.x), str(self.y) )

    def __iter__(self):
        yield float(self.x)
        yield float(self.y)


    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            raise IndexError( "Point index out of range" )

    def __setitem__(self, idx, value):
        if idx == 0:
            self.x = value
        elif idx == 1:
            self.y = value
        else:
            raise IndexError( "Point index out of range" )

    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)

    def __le__(self, other):
        return (self.x <= other.x) and (self.y <= other.y)

    def __gt__(self, other):
        return (self.x > other.x) and (self.y > other.y)

    def __ge__(self, other):
        return (self.x >= other.x) and (self.y >= other.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)

    def __add__( self, other):
        if not isinstance(other, Point):
            other = makePoint( other )
        return Point( self.x + other.x, self.y + other.y )
        # return Point( self.x + other, self.y + other )

    def __sub__( self, other):
        if isinstance(other, Point):
            return Point( self.x - other.x, self.y - other.y )
        return Point( self.x - other, self.y - other )

    def __mul__( self, other):
        if isinstance(other, Point):
            return Point( self.x * other.x, self.y * other.y )
        return Point( self.x * other, self.y * other )

    def __truediv__( self, other):
        if isinstance(other, Point):
            return Point( self.x / other.x, self.y / other.y )
        return Point( self.x / other, self.y / other )

    def asFloatPoint( self ):
        return Point( float(self.x), float(self.y))

    def asIntegerPoint( self ):
        return Point( int( round(self.x) ), int( round(self.y) ))

    def scale(self, factor):
        """
        FuncGeometry vector scale
        """
        return Point(self.x * factor, self.y * factor)

    def scale_at(self, other, factor):
        return self + ((other - self) * factor)
        # d = self - other
        # d *= factor
        # return self + d #*factor

    def as_tuple(self):
        return (self.x, self.y)

    def as_distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


    def rotate(self, deg):
        # Use NodeBox cGeo
        # np = Point(0,0)
        d = math.radians(deg)
        cd = math.cos(d)
        sd = math.sin(d)
        return Point(
            self.x * cd + self.y * sd,
            self.y * cd - self.x * sd)

    def as_angle(self, other, deg):
        # Use NodeBox cGeo
        return Point(
            self.x + (other.x * math.cos( math.radians(deg) )),
            self.y + (other.y * math.sin( math.radians(deg) )))
        """
        p = other - self
        return self + p.rotate(deg)
        """

    def corner( self, aPoint ):
        """Return a Rectangle( self, aPoint )"""
        return Rectangle( self, aPoint )

    def extent( self, aPoint ):
        """Answer a Rectangle whose origin is the receiver and whose extent is
           aPoint. This is one of the infix ways of expressing the creation of
           a rectangle."""
        return Rectangle.originExtent( self, aPoint )

    def isPoint( self ):
        return True

    def rect( self, aPoint ):
        """Answer a Rectangle that encompasses the receiver and aPoint.
           This is the most general infix way to create a rectangle."""
        return Rectangle( min(self, aPoint), max(self, aPoint ))

    def asArray( self ):
        return (self.x, self.y)

    def copy( self ):
        return Point( self.x, self.y )

    def sideOf( self, otherPoint ):
        """Returns #left, #right or #center if the otherPoint lies to the left,
           right or on the line given by the vector from 0@0 to self"""
        side = self.crossProduct( otherPoint )
        side = sign( side )
        sides = ('right', 'center', 'left')
        return sides[side+1]

    def bearingToPoint( self, anotherPoint ):
        """Return the bearing, in degrees, from the receiver to anotherPoint.
           Adapted from Playground, where the ultimate provenance of the
           algorithm was a wild earlier method of Jay Fenton's which I never
           checked carefully, but the thing has always seemed to work."""

        deltaX = anotherPoint.x - self.x
        deltaY = anotherPoint.y - self.x
        
        if abs(deltaX) < 0.001:
            if deltaY > 0:
                return 180.0
            else:
                return 0.0
        
        q = 270
        if deltaX >= 0:
            q = 90
        return q - round( math.degrees(-math.arctan(deltaY / deltaX)) )

    def crossProduct( self, aPoint ):
        """Answer a number that is the cross product of the receiver and the 
        argument, aPoint."""
        
        return (self.x * aPoint.y) - (self.y * aPoint.x)


    def dist( self, aPoint ):
        """Answer the distance between aPoint and the receiver."""
        dx = aPoint.x - self.x
        dy = aPoint.y - self.y
        return math.sqrt( (dx * dx) + (dy * dy) )

    def dotProduct( self, aPoint ):
        """Answer a number that is the dot product of the receiver and the 
        argument, aPoint. That is, the two points are multipled and the 
        coordinates of the result summed."""
        return (self.x * aPoint.x) + (self.y * aPoint.y)

    def eightNeighbors( self ):
        return [
            self + Point( 1, 0),
            self + Point( 1, 1),
            self + Point( 0, 1),
            self + Point(-1, 1),
            self + Point(-1, 0),
            self + Point(-1,-1),
            self + Point( 0,-1),
            self + Point( 1,-1)]

    def fourNeighbors( self ):
        return [
            self + Point( 1, 0),
            self + Point( 0, 1),
            self + Point(-1, 0),
            self + Point( 0,-1)]

    def flipByCenterAt( self, direction, center ):
        """Answer a Point which is flipped according to the direction about
           the point c.  Direction must be #vertical or #horizontal."""
        if direction == "vertical":
            return Point( self.x, center.y * 2 - self.y)
        elif direction == "horizontal":
            return Point( center.x * 2 - self.x, self.y )
        # raise error: 'unrecognizable direction'

    def grid( self, aPoint ):
        """Answer a Point to the nearest rounded grid modules specified
        by aPoint."""
        gridPoint = makePoint( aPoint )
        newX = round(self.x / float( gridPoint.x )) * gridPoint.x
        newY = round(self.y / float( gridPoint.y )) * gridPoint.y
        return Point(newX,newY)

    def insideTriangle( self, p1, p2, p3 ):
        """Return true if the receiver is within the triangle defined by the
           three coordinates.
           
           Note: This method computes the barycentric coordinates for the
                 receiver and tests those coordinates."""
        pass

    def normal(self):
        """Answer a Point representing the unit vector rotated
           90 deg clockwise."""
        p = Point(-self.y, self.x)
        return p / math.sqrt((p.x * p.x + p.y * p.y))

    def normalized( self ):
        r = math.sqrt((self.x ** 2) + (self.y ** 2))
        return Point( self.x / r, self.y / r)

    # BAUSTELLE
    def octantOf(self, otherPt ):
        """Return 1..8 indicating relative direction to otherPoint.
           1=ESE, 2=SSE, ... etc. clockwise to 8=ENE"""
        if (self.x == otherPt.x) and (self.y > otherPt.y):
            return 6
        if (self.y < otherPt.y) and (self.x < otherPt.x):
            return 8
        quad = self.quadrantOf( otherPt )
        moreHoriz = abs( self.x - otherPt.x) >= abs(self.y - otherPt.y)
        """
            moreHoriz _ (x - otherPoint x) abs >= (y - otherPoint y) abs.
            (quad even eqv: moreHoriz)
                ifTrue: [^ quad * 2]
                ifFalse: [^ quad * 2 - 1]! !
        """

    def onLineFromTo(self, p1, p2):
        return self.onLineFromToWithin( p1, p2, 2)

    def onLineFromToWithin( self, p1, p2, epsilon):
        """Answer true if the receiver lies on the given line segment
           between p1 and p2 within a small epsilon."""
        # is this point within the box spanning p1 and p2
        # expanded by epsilon? (optimized)
        if p1.x < p2.x:
            if (   (self.x < (p1.x - epsilon))
                or (self.x > (p2.x + epsilon))):
                return False
        else:
            if (   (self.x < (p2.x - epsilon))
                or (self.x > (p1.x + epsilon))):
                return False

        if p1.y < p2.y:
            if (   (self.y < (p1.y - epsilon)) 
                or (self.y > (p2.y + epsilon))):
                return False
        else:
            if (   (self.y < (p2.y - epsilon))
                or (self.y > (p1.y + epsilon))):
                return False

        return self.dist(self.nearestPointAlongLineFromTo(p1, p2)) <= epsilon

    def quadrantOf(self, otherPoint):
        """Return 1..4 indicating relative direction to otherPoint.
        1 is downRight, 2=downLeft, 3=upLeft, 4=upRight"""
        if  self.x <= otherPoint.x:
            if self.y < otherPoint.y:
                return 1
            else:
                return 4
        else:
            if  self.y <= otherPoint.y:
                return 2
            else:
                return 4

    def rotateByCenterAt( self, direction, c  ):
        """Answer a Point which is rotated according to direction, about the
           point c.
           Direction must be one of #right (CW), #left (CCW)
           or #pi (180 degrees)."""
        c = makePoint( c )
        offset = self - c
        if direction == "right":
            return( Point(-offset.y,  offset.x) + c )
        elif direction == "right":
            return( Point( offset.y, -offset.x) + c )
        elif direction == "pi":
            return( c - offset )
        return False    

    def sortsBefore( self, other ):
        """Return true if the receiver sorts before the other point"""
        if self.y == other.y:
            return self.x <= other.x
        else:
            return self.y <= other.y

    def squaredDistanceTo( self, aPoint ):
        """Answer the distance between aPoint and the receiver."""
        aPoint = makePoint( aPoint )
        delta = aPoint - self
        return delta.dotProduct( delta )

    def transposed( self ):
        return Point( self.y, self.x )

    def interpolateToAt( self, end, amountDone ):
        """Interpolate between the instance and end after the specified amount
           has been done (0 - 1)."""
        return self + ((end - self) * amountDone)

    def midPoint( self, otherPoint):
        """Return the point halfway between self and otherPoint"""
        return self.interpolateToAt( otherPoint, 0.5 )


    def nearestPointAlongLineFromTo( self, p1, p2 ):
        """Note this will give points beyond the endpoints.
        Streamlined by Gerardo Richarte 11/3/97"""

        if p1.x == p2.x:
            return Point(p1.x, self.y)
        if p1.y == p2.y:
            return Point( self.x, p1.y )
        x1 = float( p1.x )
        y1 = float( p1.y )
        x21 = float(p2.x) - x1
        y21 = float(p2.y) - y1
        t =  (((float(self.y) - y1) / x21
             + (float(self.x) - x1) / y21)
             / ( (x21 / y21) + (y21 / x21)))
        return Point(x1 + (t * x21)) , (y1 + (t * y21))

    def degrees( self ):
        if self.x == 0:
            if self.y >= 0:
                return 90.0
            else:
                return 270.0
        else:
            tangente = float(self.y) / float(self.x)
            theta = math.atan( tangente )
            if self.x >= 0:
                if self.y >= 0:
                    return math.degrees( theta )
                else:
                    return 360.0 + math.degrees( theta )
            else:
                return 180.0 + math.degrees( theta )

    def degreesWith( self, aPoint ):
        """Answer the angle the receiver makes with origin in degrees.
            right is 0;
            down is 90."""
        if self.x == aPoint.x:
            if self.y >= aPoint.y:
                return 0.0
            else:
                return 180.0
        else:
            tan = float(self.y - aPoint.y) / float(self.x - aPoint.x )
            thetadeg = math.degrees(math.atan( tan ))
            if self.x >= aPoint.x:
                if self.y >= aPoint.y:
                    return thetadeg
                else:
                    return 360.0 + thetadeg
            else:
                return 180.0 + thetadeg

    def r( self ):
        """Answer the receiver's radius in polar coordinate system."""
        return math.sqrt( self.dotProduct( self ) )

    def theta( self ):
        """Answer the angle the receiver makes with origin in radians.
            right is 0;
            down is 90."""
        if self.x == 0:
            if self.y >= 0:
                return math.radians( 90 )
                # return 1.5708 # 90.0 degreesToRadians
            else:
                return math.radians( 270 )
                # return 4.71239 # 270.0 degreesToRadians
        else:
            tangente = float(self.y) / float(self.x)
            theta = math.atan( tangente )
            if self.x >= 0:
                if self.y >= 0:
                    return theta
                else:
                    return math.radians( 360.0 ) + theta
            else:
                return math.radians( 180 ) + theta


    def bitShiftPoint(self, bits ):
        self.x = int(round(self.x)) << int(bits)
        self.y = int(round(self.y)) << int(bits)

    def setRDegrees(self, rho, degrees ):
        radians = math.radians( float(degrees) )
        self.x = float( rho ) * math.cos( radians )
        self.y = float( rho ) * math.sin( radians )

    def adhereTo( self, aRect ):
        """If the receiver lies outside aRectangle, return the nearest point
           on the boundary of the rectangle, otherwise return self."""
        if aRect.containsPoint( self ):
            return self
        x = min(max(self.x. aRect.left), aRect.right)
        y = min(max(self.y, aRect.top), aRect.bottom)
        return Point( x, y )

    def negated( self ):
        """Answer a point whose x and y coordinates are the negatives of
           those of the receiver.  6/6/96 sw"""
        return Point( 0-self.x, 0-self.y )

    def scaleBy( self, factorpt ):
        """Answer a Point scaled by factor (an instance of Point)."""
        return Point(self.x * factorpt.x, self.y * factorpt.y)

    def scaleFromTo(self, rect1, rect2 ):
        """Produce a point stretched according to the stretch from
           rect1 to rect2"""
        x = rect2.topLeft + ((self.x - rect1.left) * rect2.width // rect1.width)
        y = (self.y - rect1.top) * rect2.height // rect1.height
        return Point( x, y )

    def rotateByAboutCenter( self, angle, center ):
        """Even though Point.theta is measured CW, this rotates with the
           more conventional CCW interpretateion of angle."""
        p = self - center
        r = p.r
        theta = float( angle ) - p.theta
        x = float( center.x ) + ( r * math.cos( theta ))
        y = float( center.y ) - ( r * math.sin( theta ))
        return Point( x, y )

    def translateBy( self, delta ):
        """Answer a Point translated by delta (an instance of Point)."""
        delta = makePoint( delta )
        return self + delta

    def rounded( self ):
        """Answer a Point that is the receiver's x and y rounded. Answer
           the receiver if its coordinates are already integral."""
        if isinstance(self.x, int):
            if isinstance(self.y, int):
                return self
        return Point( round(self.x), round(self.y) )

    def truncateTo( self, grid ):
        """Answer a Point that is the receiver's x and y truncated to
           grid x and grid y."""
        gridPoint = makePoint(grid)
        x = (self.x // gridPoint.x) * gridPoint.x
        y = (self.y // gridPoint.y) * gridPoint.y
        return Point(x,y)

    def truncated( self ):
        """Answer a Point whose x and y coordinates are integers.
        Answer the receiver if its coordinates are already integral."""
        if (int(self.x) == self.x) and (int(self.y) == self.y ):
            return self
        return Point( int( self.x ), int(self.y) )
    def isZero( self ):
        epsilon = 0.00001
        if 0.0 - epsilon < self.x < 0.0 + epsilon:
            if 0.0 - epsilon < self.y < 0.0 + epsilon:
                return True
        return False


    @classmethod
    def rhoDegrees( cls, rho, degrees ):
        "Answer an instance of me with polar coordinates rho and degrees."
        p = cls(0,0)
        return p.setRDegrees( rho, degrees )

class Rectangle(object):
    "Translated from a Squeak 3.7 image"

    def __init__(self, origin, corner):
        p1 = makePoint( origin )
        p2 = makePoint( corner )
        if p2 < p1:
            p1, p2 = p2, p1
        self.porigin = p1
        self.pcorner = p2


    def __iter__(self):
        """Iterate all 4 corners"""
        for item in self.corners:
            yield item

    def __repr__( self ):
        return u"Rectangle( %s, %s )" % (repr(self.origin), repr(self.corner) )


    def __eq__( self, other ):
        return ((   self.origin == other.origin )
                and ( self.corner == other.corner))

    def __ne__( self, other ):
        return (self.origin != other.origin) or (self.corner != other.corner)

    def __add__( self, other):
        if isinstance(other, Rectangle):
            return Rectangle( self.origin + other.origin, self.corner + other.corner )
        elif isinstance(other, Point):
            return Rectangle( self.origin + other.x, self.corner + other.y)
        return Rectangle( self.origin + other, self.corner + other )

    def __sub__( self, other):
        if isinstance(other, Rectangle):
            return Rectangle( self.origin - other.origin, self.corner - other.corner )
        elif isinstance(other, Point):
            return Rectangle( self.origin - other.x, self.corner - other.y)
        return Rectangle( self.origin - other, self.corner - other )

    def __mul__( self, other):
        if isinstance(other, Rectangle):
            return Rectangle( self.origin * other.origin, self.corner * other.corner )
        elif isinstance(other, Point):
            return Rectangle( self.origin * other.x, self.corner * other.y)
        return Rectangle( self.origin * other, self.corner * other )

    # origin
    def getorigin(self):
        return self.porigin
    def setorigin(self, val):
        self.porigin = makePoint( val )
    origin = property(getorigin, setorigin)

    # corner
    def getcorner(self):
        return self.pcorner
    def setcorner(self, val):
        self.pcorner = makePoint( val )
    corner = property(getcorner, setcorner)

    def setOriginCorner( self, origin, corner ):
        self.origin = origin
        self.corner = corner


    # height
    def getheight(self):
        return self.corner.y - self.origin.y
    def setheight( self, height):
        self.corner.y = self.origin.y + height
    height = property(getheight, setheight)

    #  width
    def getwidth(self):
        return self.corner.x - self.origin.x
    def setwidth( self, width):
        self.corner.x = self.origin.x + width
    width = property(getwidth, setwidth)

    # area
    def getarea( self ):
        return self.width * self.height
    area = property(getarea)

    # widthheight
    def getwidthheight( self ):
        return  (self.width, self.height)

    def setwidthheight( self, width, height ):
        self.width = width
        self.height = height
        return self.getwidth, self.getheight
    widthheight = property( getwidthheight, setwidthheight )


    # top
    def gettop( self ):
        return self.origin.y
    def settop( self, val ):
        self.origin.y = val
    top = property( gettop, settop )

    # bottom
    def getbottom( self ):
        return self.corner.y
    def setbottom( self, val ):
        self.corner.y = val
    bottom = property( getbottom, setbottom )

    # left
    def getleft( self ):
        return self.origin.x
    def setleft( self, val ):
        self.origin.x = val
    left = property( getleft, setleft )

    # right
    def getright( self ):
        return self.corner.x
    def setright( self, val ):
        self.corner.x = val
    right = property( getright, setright )


    # topleft
    def gettopleft( self ):
        return self.origin
    def settopleft( self, *args):
        self.origin = makePoint( args )
    topleft = property( gettopleft, settopleft )

    # topright
    def gettopright( self ):
        return Point( self.corner.x, self.origin.y )
    def settopright( self, *args):
        p = makePoint( args )
        self.corner.x = p.x
        self.origin.y = p.y
    topright = property( gettopright, settopright )

    # bottomleft
    def getbottomleft( self ):
        return Point( self.origin.x, self.corner.y )
    def setbottomleft( self, *args):
        p = makePoint( args )
        self.origin.x = p.x
        self.corner.y = p.y
    bottomleft = property( getbottomleft, setbottomleft )

    # bottomright
    def getbottomright( self ):
        return self.corner
    def setbottomright( self, *args):
        self.corner = makePoint( args )
    bottomright = property( getbottomright, setbottomright )

    # center
    def getcenter( self ):
        return Point( self.left + self.width / 2.0,
                            self.top + self.height / 2.0 )
    def setcenter( self, *args):
        center = makePoint( args )
        ext = self.extent
        half = ext / 2.0
        self.origin = center - half
        self.corner = center + half
    center = property( getcenter, setcenter )

    # bottomcenter
    def bottomcenter( self ):
        return Point( self.center.x, self.bottom )
    bottomcenter = property( bottomcenter )

    # topcenter
    def topcenter( self ):
        return Point( self.center.x, self.top )
    topcenter = property( topcenter )

    # leftcenter
    def leftcenter( self ):
        return Point( self.left, self.center.y )
    leftcenter = property( leftcenter )

    # rightcenter
    def rightcenter( self ):
        return Point( self.right, self.center.y )
    rightcenter = property( rightcenter )

    def getcorners( self ):
        return [
            self.topleft,
            self.bottomleft,
            self.bottomright,
            self.topright
        ]
    # TODO
    def setcorners( self, topLeft, bottomleft, bottomright, topright ):
        # This is wrong should default args to None and set each separately
        self.origin( topLeft )
        self.corner( bottomRight )
    corners = property( getcorners )

    def getextent( self ):
        return self.corner - self.origin
    def setextent( self, aPoint ):
        self.corner( self.origin + aPoint )
    extent = property( getextent, setextent )


    # horizontal lines  
    def gethorizontallines(self):
        return [
            # top
            (self.topleft, self.topright),
            # bottom
            (self.bottomleft, self.bottomright)]

    def sethorizontallines( self, lines ):
        # top
        #top = makePoint(lines[0])
        #bottom = makePoint(lines[1])
        self.topleft = lines[0][0]
        self.topright = lines[0][1]
        # bottom
        self.bottomleft = lines[1][0]
        self.bottomright = lines[1][1]
    horizontallines = property( gethorizontallines, sethorizontallines )


    # vertical lines  
    def getverticallines(self):
        return [
            # left
            (self.topleft, self.bottomleft),
            # right
            (self.topright, self.bottomright)]

    def setverticallines( self, lines ):
        # left
        self.topleft = lines[0][0]
        self.bottomleft = lines[0][1]
        # right
        self.topright = lines[1][0]
        self.bottomright = lines[1][1]
    verticallines = property( getverticallines, setverticallines )


    def getTopLeftBottomRightLines( self ):
        top, bottom = self.horizontallines
        left, right = self.verticallines
        return [ top,left,bottom,right ]

    topLeftBottomRightLines = property( getTopLeftBottomRightLines )


    def withRight( self, x ):
        """Return a copy of me with a different right x"""
        return Rectangle( self.origin, Point( x, self.corner.y))

    def withLeft( self, x ):
        """Return a copy of me with a different left x"""
        return Rectangle( Point(x, self.origin.y), self.corner)

    def withBottom( self, y ):
        """Return a copy of me with a different bottom y"""
        return Rectangle( self.origin, Point( self.corner.x, y) )

    def withTop( self, y ):
        """Return a copy of me with a different top y"""
        return Rectangle( Point(self.origin.x, y), self.corner )

    def withSideSetTo( self, side, val ):
        """return a copy with side set to value"""
        if side == "left":
            return Rectangle( Point(val, self.origin.y), self.corner )
        elif side == "right":
            return Rectangle( self.origin, Point(val, self.corner.y) )
        elif side == "top":
            return Rectangle( Point(self.origin.x, val), self.corner )
        elif side == "bottom":
            return Rectangle( self.origin, Point(self.corner.x, val) )

    def withHeight( self, height ):
        """Return a copy of me with a different height"""
        return Rectangle( self.origin,
                          Point( self.corner.x, self.origin.y + height ))

    def withWidth( self, width ):
        """Return a copy of me with a different width"""
        return Rectangle( self.origin,
                          Point( self.origin.x + width, self.corner.y))

    def amountToTranslateWithin( self, otherRectangle ):
        """Answer a Point, delta, such that self + delta is forced
           within otherRectangle.

           Altered so as to prefer to keep self topLeft inside when all of self
           cannot be made to fit 7/27/96 di"""
        dx = dy = 0
        if self.right > otherRectangle.right:
            dx = otherRectangle.right - self.right

        if self.bottom > otherRectangle.bottom:
            dy = otherRectangle.bottom - self.bottom

        if (self.left + dx) < otherRectangle.left:
            dx = otherRectangle.left - self.left

        if (self.top + dy) < otherRectangle.top:
            dy = otherRectangle.top - self.top
        return Point(dx,dy)

    def areasOutside( self, otherRectangle ):
        """Answer a list of Rectangles comprising the parts of the receiver
           not intersecting otherRectangle."""

        areas = []
        
        # this is the negated overlap condition -> no overlap -> self
        if not (    (self.origin <= otherRectangle.corner)
                and (otherRectangle.origin <= self.corner)):
            return [self]

        # overlap self.top above otherRectangle.top
        if otherRectangle.origin.y > self.origin.y:
            areas.append( Rectangle( self.origin,
                                     Point(self.corner.x,
                                           otherRectangle.origin.y)) )
            yOrigin = otherRectangle.origin.y
        else:
            yOrigin = self.origin.y

        # overlap self.bottom above otherRectangle.bottom
        if otherRectangle.corner.y < self.corner.y:
            yCorner = otherRectangle.corner.y
            areas.append( Rectangle( Point(self.origin.x, yCorner ),
                                     self.corner) )
        else:
            yCorner = self.corner.y

        # overlap self.left < otherRectangle.left
        if otherRectangle.origin.x > self.origin.x:
            areas.append( Rectangle( Point(self.origin.x, yOrigin),
                                     Point(otherRectangle.origin.x, yCorner)) )

        # overlap self.right > otherRectangle.right
        if otherRectangle.corner.x < self.corner.x:
            areas.append( Rectangle( Point(otherRectangle.corner.x, yOrigin),
                                     Point(self.corner.x, yCorner) ))
        return areas

    def asArray( self ):
        return [self.origin.x,
                self.origin.y,
                self.corner.x,
                self.corner.y]

    def asPointList( self ):
        return [self.origin, self.corner]


    def bordersOnAlong( self, her, herSide ):
        if (   (herSide == b"right" and self.left == her.right)
            or (herSide == b"left"  and self.right == her.left)):
            return max(self.top, her.top) < min(self.bottom, her.bottom)

        if (   (herSide == b"bottom" and self.top == her.bottom)
            or (herSide == b"top"  and self.bottom == her.top)):
            return  max(self.left, her.left) < min(self.right, her.right)
        return False

    def encompass( self, aPointOrRect ):
        """Answer a Rectangle that contains both the receiver and aPoint.
           5/30/96 sw"""
        if type( aPointOrRect ) in (Rectangle,):
            return Rectangle( min(self.origin, aPointOrRect.origin),
                              max(self.corner, aPointOrRect.corner) )
        else:
            aPointOrRect = makepoint( aPointOrRect )
            return Rectangle( min(self.origin, aPointOrRect),
                              max(self.corner, aPointOrRect) )

    def expandBy( self, delta ):
        """Answer a Rectangle that is outset from the receiver by delta.
           delta is a Rectangle, Point, or scalar."""
        if isinstance(delta, Rectangle):
            return Rectangle( self.origin - delta.origin,
                              self.corner + delta.corner)
        else:
            return Rectangle( self.origin - delta,
                              self.corner + delta)



    def extendBy( self, delta ):
        """Answer a Rectangle with the same origin as the receiver,
           but whose corner is offset by delta. delta is a
           Rectangle, Point, or scalar."""

        if isinstance(delta, Rectangle):
            return Rectangle( self.origin, self.corner + delta.corner )
        return Rectangle( self.origin, self.corner + delta)

    def insetBy( self, delta ):
        """Answer a Rectangle that is inset from the receiver by delta.
           delta is a Rectangle, Point, or scalar."""
        if isinstance(delta, Rectangle):
            return Rectangle( self.origin + delta.origin,
                              self.corner - delta.corner )
        return Rectangle( self.origin + delta,
                          self.corner - delta)


    def insetOriginAndCornerBy( self, originDeltaPoint, cornerDeltaPoint ):
        """Answer a Rectangle that is inset from the receiver by a given
           amount in the origin and corner."""
        return Rectangle( self.origin + originDeltaPoint,
                          self.corner - cornerDeltaPoint )


    def intersect( self, otherRectangle ):
        """Answer a Rectangle that is the area in which the receiver overlaps
           with otherRectangle. Optimized for speed; old code read:
            ^Rectangle 
                origin: (origin max: otherRectangle origin)
                corner: (corner min: otherRectangle corner)
        # old code
            return Rectangle( max(self.origin, otherRectangle.origin),
                              min(sel.corner, otherRectangle.corner) )
        """

        left = right = top = bottom = 0
        
        # origin of intersection
        # aPoint = otherRectangle.origin
        x, y = otherRectangle.origin.asArray()
        left = max( x, self.origin.x )
        top = max( y, self.origin.y )

        # corner 
        # aPoint = otherRectangle.corner
        x, y = otherRectangle.corner.asArray()
        right = min( x, self.corner.x )
        bottom = min( y, self.corner.y )

        return Rectangle( (left,top), (right, bottom) )


    def merge( self, otherRectangle ):
        """Answer a Rectangle that contains both the receiver
           and otherRectangle."""
        return Rectangle( min(self.origin, otherRectangle.origin),
                          max(self.corner, otherRectangle.corner) )

    def outsetBy( self, delta ):
        """Answer a Rectangle that is outset from the receiver by delta.
           delta is a Rectangle, Point, or scalar."""
        if isinstance( delta, Rectangle ):
            return Rectangle(self.origin - delta.origin,
                             self.corner + delta.corner)
        else:
            return Rectangle(self.origin - delta,
                             self.corner + delta)


    def pointNearestTo( self, aPoint ):
        """Return the point on my border closest to aPoint"""
        side = ""
        if self.containsPoint( aPoint ):
            side = self.sideNearestTo( aPoint )
            if side == "right":
                return Point( self.right, aPoint.y )
            elif side == "left":
                return Point( self.left, aPoint.y )
            elif side == "bottom":
                return Point( aPoint.x, self.bottom )
            elif side == "top":
                return Point( aPoint.x, self.top )
        else:
            return aPoint.adhereTo( self )


    def quickMerge( self, otherRectangle ):
        """Answer the receiver if it encloses the given rectangle or the
           merge of the two rectangles if it doesn't. THis method is an
           optimization to reduce extra rectangle creations."""
        
        useReceiver = True
        rOrigin = otherRectangle.topLeft
        rCorner = otherRectangle.bottomRight

        if rOrigin.x < self.origin.x:
            useReceiver = False
            minX = rOrigin.x
        else:
            minX = self.origin.x
        
        if rCorner.x > self.corner.x:
            useReceiver = False
            maxX = rCorner.x
        else:
            maxX = self.corner.x
        
        if rOrigin.y < self.origin.y:
            useReceiver = False
            minY = r.Origin.y
        else:
            minY = self.Origin.y
        
        if rCorner.y > self.corner.y:
            useReceiver = False
            maxY = rCorner.y
        else:
            maxY = self.corner.y
        
        if useReceiver:
            return self
        else:
            return Rectangle( Point(minX, minY), Point(maxX, maxY) )

    def rectanglesAtHeight( self, y, ht ):
        if (y + ht) > self.bottom:
            return []
        return [ Rectangle( Point(self.origin.x, y),
                            Point(self.corner.x, (y+ht)) ) ]

    def sideNearestTo( self, aPoint ):
        aPoint = makePoint( aPoint )
        distToLeft = aPoint.x - self.left
        distToRight = self.right - aPoint.x
        distToTop = aPoint.y - self.top
        distToBottom = self.bottom - aPoint.y
        closest = distToLeft
        side = "left"
        if distToRight < closest:
            closest = distToRight
            side = "right"
        if distToTop < closest:
            closest = distToTop
            side = "top"
        if distToBottom < closest:
            closest = distToBottom
            side = "bottom"
        return side
            
    def translatedToBeWithin( self, otherRectangle ):
        """Answer a copy of the receiver that does not extend
           beyond otherRectangle.  7/8/96 sw"""
        return self.translatedBy( self.amountToTranslateWithin( otherRectangle ))


    def withSideOrCornerSetToPoint( self, side, newPoint ):
        """Return a copy with side set to newPoint"""
        return self.sideWithCornerSetToPointMinExtent( side,
                                                       newPoint, Point(0,0) )

    def sideWithCornerSetToPointMinExtent( self, side, newPoint, minExtent ):
        """Return a copy with side set to newPoint"""
        limit = 999999
        if side in ("left", "top"):
            limit = -999999
        return self.withSideOrCornerSetToPointMinExtentLimit( side, newPoint,
                                                            minExtent, limit )
        
        

    # unfinished - need to lookup precedence
    def withSideOrCornerSetToPointMinExtentLimit(self, side, newPoint, minExtent, limit ):
        """Return a copy with side set to newPoint"""
        if side == "top":
            # ^ self withTop: (newPoint y min: corner y - minExtent y max: limit + minExtent y)
            return self.withTop( min( newPoint.y, max(self.corner.y - minExtent.y, limit + minExtent.y ) ))

        if side == "bottom":
            # ^ self withBottom: (newPoint y min: limit - minExtent y max: origin y + minExtent y)
            return self.withBottom( min( newPoint.y, self.corner.y - max(minExtent.y, limit + minExtent.y ) ))

        if side == "left":
            # ^ self withLeft: (newPoint x min: corner x - minExtent x max: limit + minExtent x)
            return self.withLeft( min( newPoint.y, self.corner.y - max(minExtent.y, limit + minExtent.y ) ))

        if side == "right":
            # ^ self withRight: (newPoint x min: limit - minExtent x max: origin x + minExtent x)
            return self.withRight( min( newPoint.y, self.corner.y - max(minExtent.y, limit + minExtent.y ) ))

        if side == "topLeft":
            # ^ (newPoint min: corner - minExtent) corner: self bottomRight
            return Rectangle( min(newPoint, self.corner - minExtent), self.bottomRight )

        if side == "bottomRight":
            # ^ self topLeft corner: (newPoint max: origin + minExtent)
            return 

        if side == "bottomLeft":
            # ^ self topRight rect: ((newPoint x min: corner x - minExtent x) @ (newPoint y max: origin y + minExtent y))
            pass

        if side == "topRight":
            # ^ self bottomLeft rect: ((newPoint x max: origin x + minExtent x) @ (newPoint y min: corner y - minExtent y))
            pass
    """
    !Rectangle methodsFor: 'rectangle functions' stamp: 'bf 9/10/1999 16:07'!
    withSideOrCorner: side setToPoint: newPoint minExtent: minExtent limit: limit
        "Return a copy with side set to newPoint"
        side = #top ifTrue: [^ self withTop: (newPoint y min: corner y - minExtent y max: limit + minExtent y)].
        side = #bottom ifTrue: [^ self withBottom: (newPoint y min: limit - minExtent y max: origin y + minExtent y)].
        side = #left ifTrue: [^ self withLeft: (newPoint x min: corner x - minExtent x max: limit + minExtent x)].
        side = #right ifTrue: [^ self withRight: (newPoint x min: limit - minExtent x max: origin x + minExtent x)].
        side = #topLeft ifTrue: [^ (newPoint min: corner - minExtent) corner: self bottomRight].
        side = #bottomRight ifTrue: [^ self topLeft corner: (newPoint max: origin + minExtent)].
        side = #bottomLeft ifTrue: [^ self topRight rect: ((newPoint x min: corner x - minExtent x) @ (newPoint y max: origin y + minExtent y))].
        side = #topRight ifTrue: [^ self bottomLeft rect: ((newPoint x max: origin x + minExtent x) @ (newPoint y min: corner y - minExtent y))].! !
    """

    def containsPoint( self, aPoint ):
        "Answer whether aPoint is within the receiver."
        return (self.origin <= aPoint) and (aPoint < self.corner)

    def containsRect( self, aRect ):
        """Answer whether aRect is within the receiver (OK to coincide)."""
        return (aRect.origin >= self.origin) and (aRect.corner <= self.corner)

    def fullIntersects( self, otherRectangle ):
        """Answer whether otherRectangle intersects the receiver anywhere.
           Optimized
           
           old code answered:
            (origin max: otherRectangle origin) < (corner min: otherRectangle corner)"""

        if 0: # old code
            return (  max( self.origin, otherRectangle.origin )
                    < min(self.corner, otherRectangle.corner))
        else:
            if self.containsPoint( otherRectangle.origin ) or self.containsPoint( otherRectangle.corner ):
                return True

            if self.corner < otherRectangle.origin:
                return false

            rOrigin = otherRectangle.origin
            rCorner = otherRectangle.corner
            if rCorner.x <= self.origin.x:
                return False
            if rCorner.y <= self.origin.y:
                return False
            if rOrigin.x >= self.corner.x:
                return False
            if rOrigin.y >= self.corner.y:
                return False
            return True

    def hasPositiveExtent( self ):
        """Answer whether aPoint is within the receiver."""
        return (self.corner.x > self.origin.x) and (self.corner.y > self.origin.y)

    def intersects( self, otherRectangle ):
        """Answer whether otherRectangle intersects the receiver anywhere.
        Optimized

        old code answered:
            (origin max: otherRectangle origin) < (corner min: otherRectangle corner)"""
        
        # | rOrigin rCorner |
        rOrigin = otherRectangle.origin
        rCorner = otherRectangle.corner
        if rCorner.x <= self.origin.x:
            return False
        if rCorner.y <= self.origin.y:
            return False
        if rOrigin.x >= self.corner.x:
            return False
        if rOrigin.y >= self.corner.y:
            return False
        return True

    def isTall( self ):
        return self.height > self.width

    def isWide( self ):
        return self.width > self.height

    def isZero( self ):
        return self.origin.isZero() and self.corner.isZero()

    def rounded( self ):
        """Answer a Rectangle whose origin and corner are rounded."""
        return Rectangle( self.origin.rounded(), self.corner.rounded() )

    def truncateTo( self, grid ):
        """Answer a Rectangle whose origin and corner are truncated to grid x and grid y."""
        return Rectangle( self.origin.trincateTo( grid ), self.corner.truncateTo( grid ) )

    def truncated( self ):
        if int(self.origin.x) == self.origin.x:
            if int(self.origin.y) == self.origin.y:
                if int(self.corner.x) == self.corner.x:
                    if int(self.corner.y) == self.corner.y:
                        return self
        return Rectangle( self.origin.truncated(), self.corner.truncated() )

    def alignWith( self, aPoint1, aPoint2 ):
        return self.translateBy( aPoint2 - aPoint1 )

    def centeredBeneath( self, otherRectangle ):
        """Move the reciever so that its top center point coincides with the bottom
           center point of otherRectangle.  5/20/96 sw:"""
        return self.alignWith( self.topCenter, self.bottomCenter )


    def flipByCenterAt( self, direction, aPoint ):
        """Return a copy flipped #vertical or #horizontal, about aPoint."""
        return Rectangle( self.origin.flipByCenterAt( direction, aPoint ) )


    def rotateByCenterAt( self, direction, aPoint ):
        """Return a copy rotated #right, #left, or #pi about aPoint"""
        return self.origin.rotateByCenterAt( aPoint ).rect( self.corner.rotateByCenterAt( direction, aPoint))


    def scaleBy( self, scale ):
        """Answer a Rectangle scaled by scale, a Point or a scalar."""
        return Rectangle( self.origin * scale, self.corner * scale )


    def scaleFromTo( self, rect1, rect2 ):
        """Produce a rectangle stretched according to the stretch from rect1 to rect2"""
        return Rectangle( self.origin.scaleFromTo(rect1, rect2),
                          self.corner.scaleFromTo(rect1, rect2))
        

    def squishedWithin(self, otherRectangle ):
        """Return an adjustment of the receiver that fits within otherRectangle by reducing its size, not by changing its origin."""
        return Rectangle( self.origin.corner( min(self.corner, otherRectangle.bottomRight) ))


    def translateBy(self, factor ):
        """Answer a Rectangle translated by factor, a Point or a scalar."""
        return Rectangle( self.origin + factor, self.corner + factor )

    def translatedAndSquishedToBeWithin( self, otherRectangle ):
        """Return an adjustment of the receiver that fits within otherRectangle by
            - translating it to be within otherRectangle if necessary, then
            - reducing its size, if necessary"""
        return self.translatedToBeWithin( otherRectangle ).squishedWithin( otherRectangle )


    def split(self, x, y ):
        """Split rectangle at x,y. if either value is 0 or (w|h) only along the other value ist split."""
        
        splitpoint = makePoint( x, y )
        
        if (x > 0) and (x < self.width):
            topx = makePoint( x, self.origin.y )
            botx = makePoint( x, self.corner.y )
            if (y > 0) and (y < self.height):

                lefty = makePoint( self.origin.x, y )
                righty = makePoint( self.corner.x, y )
                
                tl = Rectangle( self.origin, splitpoint )
                tr = Rectangle( topx, righty )
                bl = Rectangle( lefty, botx )
                br = Rectangle( splitpoint, self.corner )
                return (tl, tr, bl, br)
            else:
                # y fails return left and right rectangle
                pass
        else:
            if (y > 0) and (y < self.height):
                # x fails - return upper and lower rectangle
                pass
            else:
                # complete failure - both values out of sight
                return []
    def innerSquare(self):
        pass


    def outerSquareRect(self):
        pass


    @classmethod
    def centerExtent(cls, centerPoint, extentPoint):
        """Answer an instance of me whose center is centerPoint and width 
           by height is extentPoint."""
        centerPoint = makePoint( centerPoint )
        extentPoint = makePoint( extentPoint )
        dx = round( extentPoint.x / 2.0 )
        dy = round( extentPoint.y / 2.0 )
        originPoint = Point( centerPoint.x - round( extentPoint.x / 2.0 ),
                             centerPoint.y - round( extentPoint.y / 2.0 ))
        cornerPoint = originPoint + extentPoint
        return cls( originPoint, cornerPoint )


    @classmethod
    def centerRadius(cls, centerPoint, radius):
        """Answer an instance of me whose center is centerPoint and
           radius is the distance to the top left point. """
        
        csquared = radius*radius
        cathedes = round(math.sqrt(csquared) / 2.0)
        rad = math.radians(225)
        delta = Point(cathedes, cathedes)
        topLeft = centerPoint - delta
        bottomRight = centerPoint + delta

        return cls( topLeft, bottomRight )


    @classmethod
    def encompassing( cls, pointList ):
        """A number of callers of encompass: should use this method."""
        topLeft = bottomRight = None
        for p in pointList:
            p = makePoint( p )
            if topLeft == None:
                topLeft = bottomRight = p
            else:
                topLeft = min( topLeft, p)
                bottomRight = max( bottomRight, p)
        return cls( topLeft, bottomRight )


    @classmethod
    def leftRightTopBottom(cls, left, right, top, bottom):
        """Answer an instance of me whose left, right, top, and bottom coordinates 
        are determined by the arguments."""
        return cls( Point(left,top), Point(right,bottom) )

    @classmethod
    def leftTopRightBottom(cls, left, top, right, bottom):
        """Answer an instance of me whose left, right, top, and bottom coordinates 
        are determined by the arguments."""
        return cls( Point(left,top), Point(right,bottom) )

    @classmethod
    def merging( cls, listOfRects ):
        """A number of callers of merge: should use this method."""
        minX = minY =  9999999
        maxX = maxY = -9999999
        for r in listOfRects:
            minX = min( minX, r.origin.x )
            minY = min( minY, r.origin.y )
            maxX = max( maxX, r.corner.x )
            maxY = max( maxY, r.corner.y )
        return cls( Point(minX, minY), Point(maxX, maxY) )

    @classmethod
    def originExtent( cls, originPoint, extentPoint ):
        """Answer an instance of me whose top left corner is originPoint and width 
           by height is extentPoint."""
        originPoint = makePoint( originPoint )
        extentPoint = makePoint( extentPoint )
        return cls( originPoint, originPoint + extentPoint )

class Form(object):
    """Translated from a Squeak 3.7 image
    Implemented as a abstraction layer to Image.
    """

    def __init__(self, width, height, mode="RGBA" ):
        width = int(width)
        height = int(height)
        self.img =  PIL.Image.new(mode, (width, height) )
        self.frame = Rectangle( (0,0), (width, height) )
        self.mode = mode
        # self.depth = mode
        self.fill = None
        self.pattern = None
        self.offset = Point(0,0)
        self.canvas = pb.canvas( width, height )


    def __repr__( self ):
        return u"Form( %.2f, %.2f, %s )" % (self.frame.width,
                                            self.frame.height,
                                            self.mode)


    # bits
    def getbits(self):
        return self.img
    def setbits(self, img):
        if type(img) == type(PIL.Image.Image):
            self.img = img
    bits = property(getbits, setbits)

    # width
    def getwidth( self ):
        s = self.bits.size
        return self.bits.size[0]
    def setwidth(self, newWidth):
        pass
    width = property(getwidth) #, setwidth)

    # height
    def getheight( self ):
        s = self.bits.size
        return self.bits.size[1]
    def setheight(self, newHeight):
        pass
    height = property(getheight) #, setheight)

    # pattern

    # fill

    # outline

    # alpha

    def center( self ):
        return self.frame.center


    @classmethod
    def extent( cls, extentPoint ):
        """Answer an instance of me whose top left corner is originPoint
           and width by height is extentPoint."""
        p = makePoint( extentPoint )
        #color=(31,31,31,255)
        form = cls(int(p.x), int(p.y), 'RGBA' )
        #draw = PIL.ImageDraw.Draw(form.img)
        #draw.rectangle( (0,0, p.x,p.y), fill=None, width=1)
        return form

    @classmethod
    def extentMode( cls, extentPoint, mode ):
        """Answer an instance of me with blank bitmap of the given
           dimensions and depth."""
        p = makePoint( extentPoint )
        return cls( int(p.x), int(p.y), mode )

    @classmethod
    def dotOfSize( cls, dotSizePoint ):
        color=(15,255)
        p = makePoint( dotSizePoint )
        form = cls(int(p.x), int(p.y), 'LA' )
        draw = PIL.ImageDraw.Draw(form.img)
        draw.ellipse( (0,0, p.x,p.y), fill=color, width=1)
        return form    


class Region:
    def __init__(self):
        self.scanlines = []



