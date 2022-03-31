py3 = False
try:
    unicode('')
except NameError:
    long = int

def makePoint( *args  ):
    "Tries to create a Point from args."
    n = len(args)
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


