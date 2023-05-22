
from . import point, rectangle, form, makepoint

Point = point.Point
Rectangle = rectangle.Rectangle
Form = form.Form

makePoint = makepoint.makePoint
imageRectangles = form.imageRectangles

point.Rectangle = Rectangle
point.makePoint = makePoint
rectangle.Point = Point
rectangle.makePoint = makePoint
form.Point = Point
form.Rectangle = Rectangle
form.makePoint = makePoint
makepoint.Point = Point

