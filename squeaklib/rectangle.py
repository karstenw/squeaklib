
# -*- coding: utf-8 -*-

from __future__ import print_function


# from . import makepoint
# makePoint = makepoint.makePoint

# from . import point
# Point = point.Point

class Rectangle(object):
    "Translated from a Squeak 3.7 image"

    def __init__(self, origin, corner):
        p1 = makePoint( origin )
        p2 = makePoint( corner )
        if p2 < p1:
            p1, p2 = p2, p1
        self.porigin = p1
        self.pcorner = p2


    def __repr__( self ):
        return u"Rectangle( %s, %s )" % (repr(self.origin), repr(self.corner) )


    def __eq__( self, other ):
        return (self.origin == other.origin) and (self.corner == other.corner)

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
        self.origin = makePoint( origin )
        self.corner = makePoint( corner )

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
    def setcorners( self, topLeft, bottomleft, bottomright, topright ):
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

    def amountToTranslateWithin( self, aRectangle ):
        """Answer a Point, delta, such that self + delta is forced
           within aRectangle.

           Altered so as to prefer to keep self topLeft inside when all of self
           cannot be made to fit 7/27/96 di"""
        dx = dy = 0
        if self.right > aRectangle.right:
            dx = aRectangle.right - self.right

        if self.bottom > aRectangle.bottom:
            dy = aRectangle.bottom - self.bottom

        if (self.left + dx) < aRectangle.left:
            dx = aRectangle.left - self.left

        if (self.top + dy) < aRectangle.top:
            dy = aRectangle.top - self.top
        return Point(dx,dy)

    def areasOutside( self, aRectangle ):
        """Answer an Array of Rectangles comprising the parts of the receiver
           not intersecting aRectangle."""

        areas = []
        
        # this is the negated overlap condition -> no overlap -> self
        if not (    (self.origin <= aRectangle.corner)
                and (aRectangle.origin <= self.corner)):
            #print("self")
            return [self]

        # overlap
        if aRectangle.origin.y > self.origin.y:
            yOrigin = aRectangle.origin.y
            #print("other origin y is higher; append")
            areas.append( Rectangle( self.origin,
                                     Point(self.corner.x, yOrigin)) )
        else:
            #print("self origin y is higher")
            yOrigin = self.origin.y

        if aRectangle.corner.y < self.corner.y:
            yCorner = aRectangle.corner.y
            #print("self corner y higher; append")
            areas.append( Rectangle( Point(self.origin.x, yCorner ),
                                     self.corner) )
        else:
            #print("self corner y lower")
            yCorner = self.corner.y

        if aRectangle.origin.x > self.origin.x:
            #print("other origin x more right; append")
            areas.append( Rectangle( Point(self.origin.x, yOrigin),
                                     Point(aRectangle.origin.x, yCorner)) )

        if aRectangle.corner.x < self.corner.x:
            #print("self corner more right; append")
            areas.append( Rectangle( Point(aRectangle.corner.x, yOrigin),
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


    def intersect( self, aRectangle ):
        """Answer a Rectangle that is the area in which the receiver overlaps
           with aRectangle. Optimized for speed; old code read:
            ^Rectangle 
                origin: (origin max: aRectangle origin)
                corner: (corner min: aRectangle corner)"""
        if 0: # old code
            return Rectangle( max(self.origin, aRectangle.origin),
                              min(sel.corner, aRectangle.corner) )
        else:
            left = right = top = bottom = 0
            aPoint = aRectangle.origin
            if aPoint.x > origin.x:
                left = aPoint.x
            else:
                left = origin.x

            if aPoint.y > origin.y:
                top = aPoint.y
            else:
                top = origin.y

            aPoint = aRectangle.corner
            if aPoint.x < self.corner.x:
                right = aPoint.x
            else:
                right = self.corner.x
            
            if aPoint.y < corner.y:
                bottom = aPoint.y
            else:
                bottom = corner.y
            return Rectangle( (left,top), (right, bottom) )


    def merge( self, aRectangle ):
        """Answer a Rectangle that contains both the receiver
           and aRectangle."""
        return Rectangle( min(self.origin, aRectangle.origin),
                          max(self.corner, aRectangle.corner) )

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


    def quickMerge( self, aRectangle ):
        """Answer the receiver if it encloses the given rectangle or the
           merge of the two rectangles if it doesn't. THis method is an
           optimization to reduce extra rectangle creations."""
        
        useReceiver = True
        rOrigin = aRectangle.topLeft
        rCorner = aRectangle.bottomRight

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
            
    def translatedToBeWithin( self, aRectangle ):
        """Answer a copy of the receiver that does not extend
           beyond aRectangle.  7/8/96 sw"""
        return self.translatedBy( self.amountToTranslateWithin( aRectangle ))


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

    def fullIntersects( self, aRectangle ):
        """Answer whether aRectangle intersects the receiver anywhere.
           Optimized
           
           old code answered:
            (origin max: aRectangle origin) < (corner min: aRectangle corner)"""

        if 0: # old code
            return (  max( self.origin, aRectangle.origin )
                    < min(self.corner, aRectangle.corner))
        else:
            if self.containsPoint( aRectangle.origin ) or self.containsPoint( aRectangle.corner ):
                return True

            if self.corner < aRectangle.origin:
                return false

            rOrigin = aRectangle.origin
            rCorner = aRectangle.corner
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

    def intersects( self, aRectangle ):
        """Answer whether aRectangle intersects the receiver anywhere.
        Optimized

        old code answered:
            (origin max: aRectangle origin) < (corner min: aRectangle corner)"""
        
        # | rOrigin rCorner |
        rOrigin = aRectangle.origin
        rCorner = aRectangle.corner
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

    def centeredBeneath( self, aRectangle ):
        """Move the reciever so that its top center point coincides with the bottom
           center point of aRectangle.  5/20/96 sw:"""
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
        

    def squishedWithin(self, aRectangle ):
        """Return an adjustment of the receiver that fits within aRectangle by reducing its size, not by changing its origin."""
        return Rectangle( self.origin.corner( min(self.corner, aRectangle.bottomRight) ))


    def translateBy(self, factor ):
        """Answer a Rectangle translated by factor, a Point or a scalar."""
        return Rectangle( self.origin + factor, self.corner + factor )

    def translatedAndSquishedToBeWithin( self, aRectangle ):
        """Return an adjustment of the receiver that fits within aRectangle by
            - translating it to be within aRectangle if necessary, then
            - reducing its size, if necessary"""
        return self.translatedToBeWithin( aRectangle ).squishedWithin( aRectangle )


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
        dx = round( extentPoint.x / 2.0 )
        dy = round( extentPoint.y / 2.0 )
        originPoint = Point( centerPoint.x - round( extentPoint.x / 2.0 ),
                             centerPoint.y - round( extentPoint.y / 2.0 ))
        cornerPoint = originPoint + extentPoint
        return cls( originPoint, cornerPoint )


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
        return cls( originPoint, originPoint + extentPoint )

