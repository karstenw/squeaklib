py3 = False
try:
    unicode('')
except NameError:
    long = int

def makePoint( *args  ):
    "Tries to create a Point from args."
    from . import point
    n = len(args)
    if n == 1:
        typ = type( args[0] )
        if typ in (point.Point,):
            return args[0]
        elif typ in (long, int, float):
            return point.Point( args[0], args[0] )
        elif typ in (list, tuple):
            return point.Point( args[0][0], args[0][1] )
    elif n == 2:
        return point.Point( args[0], args[1] )
    return None


