
from . import point, rectangle, form

Point = point.Point
Rectangle = rectangle.Rectangle
Form = form.Form

point.Rectangle = Rectangle
rectangle.Point = Point
form.Point = Point
form.Rectangle = Rectangle


