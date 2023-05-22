
# -*- coding: utf-8 -*-

from __future__ import print_function

import random
import pprint
pp = pprint.pprint

import PIL
import PIL.Image
import PIL.ImageDraw as ImageDraw

import pdb

import photobot as pb

from . import makepoint
makePoint = makepoint.makePoint

from . import point
Point = point.Point

from . import rectangle
Rectangle = rectangle.Rectangle

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


def imageRectangles( reclist, frame=(10,10) ):
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
    f.canvas.export("RectangleList()_" + pb.datestring(), unique=True  )

