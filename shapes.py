import math
from geometry import Matrix, Vector, Polyline, Connection, getIntersection

global precision
precision = .05

def printPrecision():
    print precision

####  SHAPE  ###################################################################################
class Shape: ###################################################################################
    polylines = []
    connections = []
    size = 0

    #### INITIATION #####======================================================================
    # Initialized vector as (0,0)
    def __init__(self, polylines=[], connections=[]):
        self.polylines = polylines
        self.connections = connections
#        print polylines
#        print list(polylines)
#        print self.polylines
#        print list(self.polylines)
        if self.polylines == []:
            self.size = 0
        else:
            self.size = len(list(self.polylines))
    
    ##### OPERATORS #####=======================================================================
    def __repr__(self):
        if self.size > 0:
            string = "This shape contains:\n"
            print len(self.polylines)
            for polyine in self.polylines:
                string += str(polyine)
                print string
            return string
        else:
            return "This shape is empty..."
                
    # Inequalities
    def __lt__(self, other):
        return self.size <  other.size
    def __le__(self, other):
        return self.size <= other.size
    def __eq__(self, other):
        return self.size == other.size
    def __ne__(self, other):
        return self.size != other.size
    def __gt__(self, other):
        return self.size >  other.size
    def __ge__(self, other):
        return self.size >= other.size
    
    # Sums etc
    def __add__(self, other):
        if isinstance(other, Vector):
            return Shape( list( polyline + other for polyline in self.polylines ), list(self.connections))
        elif isinstance(other, Shape):
            return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Shape( list( polyline - other for polyline in self.polylines ), list(self.connections))
        elif isinstance(other, Shape):
            return NotImplemented
    def __mul__(self, other):
        return Shape( list( polyline*other for polyline in self.polylines ), list(self.connections))
    def __div__(self, scalar):
        if scalar == 0:
            print "Error, tried to divide by zero!"
            return Vector(0,0)
        else:
            return Shape( list( polyline/other for polyline in self.polylines ), list(self.connections))
    def __neg__(self):
        return NotImplemented
    def __pos__(self):
        return NotImplemented
    def __abs__(self):
        return NotImplemented
    
    ##### FUNCTIONS #####=======================================================================
    def add(self, polyline):
        if polyline.size > 0:
            self.polylines += [polyline]
            self.size += 1

    def plot(self):
        for polyine in self.polylines:
            polyine.plot()


    def getBoundingBox(self):
        if self.size >= 1:
            [bbll, bbur] = self.polylines[0].getBoundingBox()   # Error check!
            
            for polyline in self.polylines:
                [bbll2, bbur2] = polyline.getBoundingBox()
#                print "Before: ", [bbll, bbur], [bbll2, bbur2]
                if  bbur.x < bbur2.x:
                    bbur.x = bbur2.x
                if bbll.x > bbll2.x:
                    bbll.x = bbll2.x
                if  bbur.y < bbur2.y:
                    bbur.y = bbur2.y
                if bbll.y > bbll2.y:
                    bbll.y = bbll2.y
#                print "After:  ", [bbll, bbur]
            return [bbll, bbur]
        else:
            return None

    def sizeCalc(self):
        self.size = len(self.polylines)
        return self.size

#    def addThickenedPolyline(self):
#
#    def addCircle(self):
#    
#    def union(other):

def linear(p0, p1, p=precision):
    toReturn = Polyline([], False)
    
    steps = int(math.ceil((p1-p0).norm()/p))
    
    toReturn.add(p0.copy())
    
    for i in range(1,steps):
        t = float(i)/steps
        toReturn.add( p0*(1.0-t) + p1*t )
    
    toReturn.add(p1.copy())

    return toReturn

def qBezier(p0, p1, p2, p=precision):   # See wikipedia
    toReturn = Polyline([], False)  # Really odd bug if this is replaced with 'Polyline()'
    
    estimatedLength = (p1-p0).norm() + (p2-p1).norm()
    steps = int(math.ceil(estimatedLength/p))
    
    toReturn.add(p0.copy())
    
    for i in range(1,steps):
        t = float(i)/steps
        toReturn.add( p0*((1.0-t)*(1.0-t)) + p1*(2.*(1.0-t)*t) + p2*(t*t) )
    
    toReturn.add(p2.copy())

    return toReturn
                
def cBezier(p0, p1, p2, p3, p=precision):   # See wikipedia
    toReturn = Polyline([], False)
    
    estimatedLength = (p1-p0).norm() + (p2-p1).norm() + (p3-p2).norm()
    steps = int(math.ceil(estimatedLength/p))
    
    toReturn.add(p0.copy())
                
    for i in range(1,steps):
        t = float(i)/steps
        toReturn.add( p0*((1.0-t)*(1.0-t)*(1.0-t)) + p1*(3*(1.0-t)*(1.0-t)*t) + p2*(3*(1.0-t)*t*t) + p3*(t*t*t) )
    
    toReturn.add(p3.copy())

    return toReturn

def getRoot(a,b,c,s=1):
#    print a, b*b - 4*a*c
    if a != 0 and b*b - 4*a*c > 0:   return (-b + s*math.sqrt(b*b - 4*a*c))/(2*a)
    else:                           return None

def connect(i_, f_, type="CIRCULAR", di=None, df=None):    # "LINEAR", "QBEZIER", "CBEZIER", "CIRCULAR", "MONOCIRCULAR"
    if isinstance(i_, Connection):
        i =  i_.v
        di = i_.dir
    else:
        i = i_

    if isinstance(f_, Connection):
        f =  f_.v
        df = f_.dir
    else:
        f = f_

    if type == "LINEAR" or di == None or df == None:
        return Polyline([i, f], False)
    elif di * df == 1 and abs(di * (f-i).unit()) == 1:
        return Polyline([i, f], False)
    elif di * df == -1 and abs(di * (f-i).unit()) == 1:
        print "Sorry, can't make this path"
        return None
    else:
        # Check if norm is zero?
        di.Unit()
        df.Unit()
        
        if   type == "QBEZIER":
            c = getIntersection(i, di, f, df)
            
            if c is not None:
                return qBezier(i, c, f)
            else:
                print "Error: Intersection could not be found; returning linear path"
                return Polyline([i, f], False)
        elif type == "CBEZIER":
            c = getIntersection(i, di, f, df)
            return NotImplemented
        elif type == "CIRCULAR":
            # Find the Radius of the two circles (confusing math that I won't explain):
            D =  f -  i
            rlist = [None, None, None, None]
            
            j = 0
            for d in [df.perp() - di.perp(), df.perp() + di.perp()]:
                a = (d.norm2() - 4)
                b = 2*(d*D)
                c = D.norm2()
                
                rlist[j] =      getRoot(a,b,c,s=1)
                rlist[j-1] =    getRoot(a,b,c,s=-1)
            
                j += 2
            
#            d = df.perp() - di.perp()
#            # Solve (d.norm2() - 4)*r^2 + 2*(d*D)*r + D.norm2()
#            if 2*(d.norm2() - 4) != 0 and 4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2() >= 0:
#                r[0] = ( -2*(d*D) + math.sqrt(4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2()) ) / ( 2*(d.norm2() - 4) )
#                r[1] = ( -2*(d*D) - math.sqrt(4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2()) ) / ( 2*(d.norm2() - 4) )
#            
#            d = df.perp() + di.perp()
#            if 2*(d.norm2() - 4) != 0 and 4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2() >= 0:
#                r[2] = ( -2*(d*D) + math.sqrt(4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2()) ) / ( 2*(d.norm2() - 4) )
#                r[3] = ( -2*(d*D) - math.sqrt(4*(d*D)*(d*D) - 4*(d.norm2() - 4)*D.norm2()) ) / ( 2*(d.norm2() - 4) )

            print rlist

            minr = "inf"
            minj = -1
            for j in range(0,3):
                if rlist[j] != None and abs(rlist[j]) < minr:
                    minr = abs(rlist[j])
                    minj = j
          
            # With knowledge of the radius, find the centers
            r = minr
            if   minj == 0 or minj == 1:
#                print i
#                print di.perp()*r
                ci = i + di.perp()*r
                cf = f + df.perp()*r
                
                print (cf - ci).norm2(), 4*r*r
                
                if (cf - ci).norm2() != 4*r*r:
                    ci = i - di.perp()*r
                    cf = f - df.perp()*r
                
                    print (cf - ci).norm2(), 4*r*r
                    
                    if (cf - ci).norm2() != 4*r*r:
                        print "Error occured with radius checking"
                        return None
            elif minj == 2 or minj == 3:
                ci = i + di.perp()*r
                cf = f - df.perp()*r
                
                print (cf - ci).norm2(), 4*r*r
                
                if (cf - ci).norm2() != 4*r*r:
                    ci = i + di.perp()*r
                    cf = f - df.perp()*r
                
                    print (cf - ci).norm2(), 4*r*r
                    
                    if (cf - ci).norm2() != 4*r*r:
                        print "Error occured with radius checking"
                        return None
            else:
                # No radius found...
                print "Sorry, can't find two minimum circles"
                return None
            
            midpoint = (ci + cf)/2

            toReturn = Polyline()
            
            toReturn.add(arc(ci, i, midpoint))
            toReturn.add(arc(ci, midpoint, f))
        
            return toReturn

        elif type == "MONOCIRCULAR":
            c = getIntersection(i, di, f, df)
            
            toReturn = Polyline()
            
            if (c - i).norm2() < (c - f).norm2():
                if (c - i) * di == 0:
                    print "CIRCULAR would be better for this case; returning linear in the meantime..."
                    return Polyline([i, f], False)
                elif (c - i) * di > 0 and (f - c) * df > 0:
                    midpoint = c - df*( (c-i).norm() )
                
                    toReturn.add(arc(c, i, midpoint))
                    toReturn.add(f)
                elif (c - i) * di < 0 and (f - c) * df < 0:
                    midpoint = c - df*( (c-i).norm() )
                    
                    toReturn.add(arc(c, i, midpoint))
                    toReturn.add(f)

            return NotImplemented

#def connectThickened(i, f):
#    connect(i.v, f.v, "CIRCULAR", )

def calcWidth(t, type, params):
    if   type == 0:
        return (t*params[0] + (1.-t)*params[1])/2.
    elif type == 1:
        return ((params[1] - params[0])*(3*t*t - 2*t*t*t) + params[0])/2.
    elif type == 2:
        return NotImplemented
    elif type == 3:
        return eval(params)
    elif type == 4:
        return params

widthTypes =    {"LINEAR":0,    "CUBIC":1,  "SPLINE":2,         "FUNCTION":3, "CONSTANT":4}
filletTypes =   {"SHARP":0,     "ROUND":1,  "BLUNT":2,          "QBEZIER":3}
capTypes =      {"FLAT":0,      "ROUND":1,  "ROUNDRECESSED":2}

def thickenPolyline(polyline_,
                    widthType_="CUBIC",  # "LINEAR", "CUBIC", "SPLINE", "FUNCTION", "CONSTANT"
                    widthParams=1.0,     # Single number (constant width), or list [ i, f ], or (in the case of "FUNCTION") a string, "CONSTANT" only uses the first value.
                    filletType_="SHARP", # "ROUND", "SHARP", "BLUNT", "QBEZIER"     !! NotImplemented
                    capType_="FLAT"):    # "FLAT", "ROUND", "ROUNDRECESSED"         !! NotImplemented
    
    
    if isinstance(polyline_, list):
        [polyline, di, df] = polyline_
    else:
        polyline = polyline_
        di = None
        df = None
    
    if isinstance(widthType_, str):     widthType = widthTypes[widthType_]
    if isinstance(filletType_, str):    filletType = filletTypes[filletType_]
    if isinstance(capType_, str):       capType = capTypes[capType_]
    
    if isinstance(widthParams, list):
        if widthType == 4: # CONSTANT
            widthParams = widthParams[0]
    elif isinstance(widthParams, str):
        if widthType != 3:
            print "Error, given function string, but not function type..."
    else:
         widthType = 4  # CONSTANT

#    print widthType, widthParams

    length = polyline.length()
    currentLength = 0
    
    if widthType == 1 or widthType == 2 or widthType == 3:
        for i in range(0, polyline.size - 1):       # Check here...
            segmentLength = (polyline.points[i] - polyline.points[i-1]).norm()
            if segmentLength > 2*precision:
                print "Length short, adding linear"
                addition = linear(polyline.points[i], polyline.points[i-1])
                polyline.points = polyline.points[0:i] + addition.points[1:addition.size - 1] + polyline.points[i+1:]
                polyline.size = len(polyline.points)
    
    
    toReturn = Polyline([], True)

    toReturn.add(polyline.perp(0, filletType, calcWidth(0, widthType, widthParams), di))
    
    for i in range(1, polyline.size - 1):
        currentLength += (polyline.points[i] - polyline.points[i-1]).norm()
        t = currentLength/length
#        print t, calcWidth(t, widthType, widthParams), (polyline.points[i] - polyline.points[i-1])
        toReturn.add(polyline.perp(i, filletType, calcWidth(t, widthType, widthParams)))
    
    toReturn.add(polyline.perp(polyline.size - 1, filletType, calcWidth(1, widthType, widthParams), df))
    
    toReturn.add(polyline.perp(polyline.size - 1, filletType, -calcWidth(1, widthType, widthParams), df))
    
    for i in range(polyline.size - 2, 0, -1):
        currentLength -= (polyline.points[i] - polyline.points[i-1]).norm()
        t = currentLength/length
#        print t, calcWidth(t, widthType, widthParams)
        toReturn.add(polyline.perp(i, filletType, -calcWidth(t, widthType, widthParams)))

    toReturn.add(polyline.perp(0, filletType, -calcWidth(0, widthType, widthParams), di))

#    print toReturn
    return toReturn



def circle(c, r, p=precision):
    if r < p:
        steps = 8
    else:
        steps = int(math.ceil(2*math.pi*r/p))
    
    toReturn = Polyline([], True)

    v = Vector(0,r)
    m = Matrix(2*math.pi/steps)
    
    for i in range(0,steps):
        v *= m
        toReturn.add(c + v)

#    print toReturn
    return toReturn

def rect(a, b):
    return Polyline([a, a + Vector(0,b.y - a.y), b, a + Vector(b.x - a.x, 0)], True)

def arc(c, i, f, chooseShortArc=True, p=precision):
    r1 = (i - c).norm()
    r2 = (f - c).norm()
    
    if r1 != r2:
        print "Can't make an arc with two radii... Choosing smallest radius"
        return None
    
    r = ( r1 if r1 < r2 else r2);
    
    dir = (f - i).cross(i - c)

    if dir == 0:
        dir = 1
        print "Arcs are equidistant, choosing CCW as shortest"

    ang = dir*math.acos(((i - c).Unit()) * ((f - c).Unit()))
    ang = (ang if chooseShortArc else ang - 2*math.pi)
    
    if r < p:
        steps = 8
    else:
        steps = int(math.ceil(abs(ang)*r/p))

    toReturn = Polyline([], False)
    
    if steps > 0:
        v = (i - c)
        m = Matrix(ang/steps)
            
        toReturn.add(i)

        for i in range(0,steps-1):
            v *= m
            #        print center + v
            toReturn.add(c + v)

        toReturn.add(f)

#    print toReturn
    return toReturn



