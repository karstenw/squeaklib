
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import math
import pprint
pp = pprint.pprint

import PIL
import PIL.Image
import PIL.ImageDraw as ImageDraw

import pdb

# makePoint Point Rectangle
from squeaklib import *

import photobot as pb




# areasoutside

cases = (
    # regular
    (Rectangle( (10,10), (190,190) ), Rectangle( (100,100), (290,290) )),
    # regular 2
    (Rectangle( (10,10), (250,250) ), Rectangle( (50,50), (190,290) )),
    # r2 in r1
    (Rectangle( (10,10), (290,290) ), Rectangle( (100,100), (140,190) )),
    # r1 in r2
    (Rectangle( (50,50), (190,190) ), Rectangle( (10,10), (290,290) )),
    # no overlap
    (Rectangle( (10,10), (90,90) ), Rectangle( (100,100), (290,290) )))

for j,case in enumerate(cases):
    #print("\n\nCASE: %i" % j) 
    r1, r2 = case
    res = r1.areasOutside( r2 )
    # pp(res)
    allrects = [r1, r2 ]
    allrects.extend( res )

    frame = Rectangle.merging( allrects )
    frame = frame.outsetBy( 20 )

    # create the canvas
    c = pb.canvas( frame.width, frame.height)
    c.fill( (255,255,255, 255) )

    x1,y1,x2,y2 = r1.asArray()
    w, h = r1.width, r1.height
    c.fill( (45, 170, 0, 64), x1, y1, w, h )

    x1,y1,x2,y2 = r2.asArray()
    w, h = r2.width, r2.height
    c.fill( (170, 45, 0, 64), x1, y1, w, h )
    #print()
    for frameit in (0,1):
        for i,r in enumerate(allrects):
            x1,y1,x2,y2 = r.asArray()
            w, h = r.width, r.height
            c.fill( (15, 15, 90+i*10, 31), x1, y1, w, h )
            if (i>1) and frameit:
                #print( "(%i, %i) , (%i, %i)  w:%i  h:%i" % (x1,y1,x2,y2,w,h))
                draw = PIL.ImageDraw.Draw(c.top.img)
                draw.rectangle( (0,0, w,h), fill=(0,0,127,127),
                                outline=(0,0,0,255), width=1)
        c.export("%i Rectangle.areasOutside(%i)" % (j,frameit) )

