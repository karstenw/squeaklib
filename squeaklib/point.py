
# -*- coding: utf-8 -*-

from __future__ import print_function


import math

import pprint
pp = pprint.pprint

import pdb

# from . import makepoint
# makePoint = makepoint.makePoint

# from . import rectangle
# Rectangle = rectangle.Rectangle

def sign( number ):
    """I can't believe that Python does not have a sign() function."""

    if number > 0:
        return +1
    elif number < 0:
        return -1
    return 0


class Point(object):
    "Translated from a Squeak 3.7 image"
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __repr__( self ):
        return u"Point( %.2f, %.2f )" % (float(self.x), float(self.y) )

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
        if isinstance(other, Point):
            return Point( self.x + other.x, self.y + other.y )
        return Point( self.x + other, self.y + other )

    def __sub__( self, other):
        if isinstance(other, Point):
            return Point( self.x - other.x, self.y - other.y )
        return Point( self.x - other, self.y - other )

    def __mul__( self, other):
        if isinstance(other, Point):
            return Point( self.x * other.x, self.y * other.y )
        return Point( self.x * other, self.y * other )

    def asFloatPoint( self ):
        return Point( float(self.x), float(self.y))

    def asIntegerPoint( self ):
        return Point( int( round(self.x) ), int( round(self.y) ))

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
        return [self.x, self.y]

    def copy( self ):
        return Point( self.x, self.y )

    def sideOf( self, otherPoint ):
        """Returns #left, #right or #center if the otherPoint lies to the left,
           right or on the line given by the vector from 0@0 to self"""
        side = self.crossProduct( otherPoint )
        side = sign( side )
        sides = ('right', 'center', 'left')
        return sides[side+1]

    def interpolateToAt( self, end, amountDone ):
        """Interpolate between the instance and end after the specified amount
           has been done (0 - 1)."""
        return self + ((end - self) * amountDone)

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

    def skalarPointOnLine( self, p1, p2, t ):
        """return the point p1 + (t * (p2-p1))
        kw 2021-02-25"""
        if t > 1.0:
            return p2
        elif t < 0.0:
            return p1
        
        dist = p2 - p1
        return p1 + (t * dist)

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


