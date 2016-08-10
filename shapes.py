import math
from geometry import Matrix, Vector, Polyline, Connection, getIntersection, plotLine, sign

global precision
#precision = .05
#precision = 1
#precision = .05
precision = .5

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
            return Shape( list( polyline + other for polyline in self.polylines ), list( connection + other for connection in self.connections ))
        elif isinstance(other, Shape):
            return Shape( self.polylines + other.polylines, self.connections + other.connections)
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Shape( list( polyline - other for polyline in self.polylines ), list( connection - other for connection in self.connections ))
        elif isinstance(other, Shape):
            return NotImplemented
    def __mul__(self, other):
        return Shape( list( polyline*other for polyline in self.polylines ), list( connection*other for connection in self.connections ))
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
    def add(self, other):
        if isinstance(other, Polyline):
            if other.size > 0:
                self.polylines += [other]
                self.size += 1
        elif isinstance(other, Shape):
            for polyline in other.polylines:
                self.polylines += [polyline]
                self.size += 1

    def plot(self):
        for polyine in self.polylines:
            polyine.plot()

    def setMaterial(self, material):
        for polyline in self.polylines:
            polyline.material = material;
        return self

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

    def intersect(self, other):
        if isinstance(other, Polyline):
#            print "isPolyline"
            toReturn = other.copy();
            
            for polyline in self.polylines:
                print polyline
                toReturn = (polyline).intersect(toReturn);

            return toReturn;


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
    
    if steps > 1e4:          # Arbitrary, check this....
        return Polyline([], False)
    
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

    if i == f:
        print "Error: There is no distance to connect..."
        return None

    if type == "LINEAR" or di == None or df == None:
        return Polyline([i, f], False)
    elif di * df == -1 and abs(di * (f-i).unit()) == 1:
        return Polyline([i, f], False)
    elif di * df == 1 and abs(di * (f-i).unit()) == 1:
        print "Sorry, can't make this path"
        return None
    else:
        # Check if norm is zero?
        di.Unit()
        df.Unit()
        
        if   type == "QBEZIER":
            c = getIntersection(i, di, f, df)
            
            if c is not None:
                if (c-i)*di > 1e-10 and (c-f)*df > 1e-10:
                    print (c-i)*di, (c-f)*df
                    return qBezier(i, c, f)
        
            print "Error: Intersection could not be found; returning linear path"
            return None #Polyline([i, f], False)
        elif type == "CBEZIER":
            l = (f - i).norm()/2
#            c = getIntersection(i, di, f, df)
            return cBezier(i, i + di*l, f + df*l, f);
        elif type == "CIRCULAR":
            # Find the Radius of the two circles (confusing math that I won't explain):
            D =  f -  i
            
            
            d = df.perp() - di.perp()
            a = (d.norm2() - 4)
            b = 2*(d*D)
            c = D.norm2()
            
            lList = [None, None, None, None]
            paramList = [None, None, None, None]
            rlist = [getRoot(a,b,c,1), getRoot(a,b,c,-1)]
            
            print rlist

            j = 0
            for r in rlist:
                for s in [1, -1]:
                    if r != None:
                        ci = i + di.perp()*(s*r)
                        cf = f + df.perp()*(s*r)
                        
                        m = (ci + cf)/2
                        
                        if abs((cf - ci).norm2() - 4*r*r) < 1e-6:
                            lList[j] = abs(r)*(abs(getArcAng(ci, i, m, (m-i)*di > 0)) + abs(getArcAng(cf, m, f, (m-f)*df > 0)))

                    j += 1

            minl = "inf"
            minj = -1
            for j in range(0,4):
#                print j, lList[j]
                if lList[j] != None and lList[j] < minl:
                    minl = lList[j]
                    minj = j

            j = 0
            for r in rlist:
                for s in [1, -1]:
                    if j == minj:
                        ci = i + di.perp()*(s*r)
                        cf = f + df.perp()*(s*r)
                        
                        m = (ci + cf)/2

                        toReturn = Polyline()
                        toReturn.add(arc(ci, i, m, (m-i)*di > 0))
                        toReturn.add(arc(cf, m, f, (m-f)*df > 0))

                        return toReturn

                    j += 1
#            return toReturn

#            r1 = getRoot(a,b,c,1)
#            
#            ci1 = i - di.perp()*r1
#            cf1 = f - df.perp()*r1
#            
#            if abs((cf1 - ci1).norm2() - 4*r1*r1) > 1e-6:
#                ci1 = i + di.perp()*r1
#                cf1 = f + df.perp()*r1
#            
#            m1 = (ci1 + cf1)/2
#            l1 = getArcAng(ci1, i, m1, (m1-i)*di > 0) + getArcAng(cf1, m1, f, (m1-f)*df > 0)
#
#
#            r2 = getRoot(a,b,c,-1)
#            
#            ci2 = i + di.perp()*r2
#            cf2 = f + df.perp()*r2
#            
#            if abs((cf1 - ci1).norm2() - 4*r2*r2) > 1e-6:
#                ci2 = i - di.perp()*r2
#                cf2 = f - df.perp()*r2
#
#            m2 = (ci1 + cf1)/2
#            l2 = getArcAng(ci2, i, m2, (m2-i)*di > 0) + getArcAng(cf2, m2, f, (m2-f)*df > 0)
#
#            if r1*l1 < r2*l2:
#                m = m1
#                ci = ci1
#                cf = cf1
#            else:
#                m = m2
#                ci = ci2
#                cf = cf2


            
#            for d in [df.perp() - di.perp()]: #, df.perp() + di.perp()]:
#                a = (d.norm2() - 4)
#                b = 2*(d*D)
#                c = D.norm2()
#                
#                rlist[j] =      getRoot(a,b,c,1)
#                rlist[j-1] =    getRoot(a,b,c,-1)
#            
#                j += 2
#            
#            print rlist
#
#            minr = "inf"
#            minj = -1
#            for j in range(0,3):
#                if rlist[j] != None and abs(rlist[j]) < minr:
#                    minr = abs(rlist[j])
#                    minj = j
#
##            minjList = []
##
##            for j in range(0,3):
##                if rlist[j] != None and abs(rlist[j]) == minr:
##                    minjList += [j]
##
##            if len(minjList) > 1:
##                for j in minrList:
#
#
#            # With knowledge of the radius, find the centers
#            r = minr
#            print r
#            if minj == 0 or minj == 1:
##                print i
##                print di.perp()*r
#                ci = i + di.perp()*r
#                cf = f + df.perp()*r
#                
#                print (cf - ci).norm2()- 4*r*r
#
##                print (cf - ci).norm2(), 4*r*r
#
#                if abs((cf - ci).norm2() - 4*r*r) > 1e-6:    # Arbitrary error!
#                    ci = i - di.perp()*r
#                    cf = f - df.perp()*r
#                
##                    print (cf - ci).norm2(), 4*r*r
#                    print (cf - ci).norm2()- 4*r*r
#
#                    if abs((cf - ci).norm2() - 4*r*r) > 1e-6:    # Arbitrary error!
#                        print "Error occured with radius checking"
#                        return None
#            elif minj == 2 or minj == 3:
#                ci = i + di.perp()*r
#                cf = f - df.perp()*r
#                
##                print (cf - ci).norm2(), 4*r*r
#                print (cf - ci).norm2()- 4*r*r
##                print "here"
#
#                if abs((cf - ci).norm2() - 4*r*r) > 1e-6:    # Arbitrary error!
##                    print "here2"
#                    ci = i - di.perp()*r
#                    cf = f + df.perp()*r
#                
##                    print (cf - ci).norm2(), 4*r*r
#                    print (cf - ci).norm2()- 4*r*r
#
#                    if abs((cf - ci).norm2() - 4*r*r) > 1e-6:    # Arbitrary error!
#                        print "Error occured with radius checking"
#                        return None
#            else:
#                # No radius found...
#                print "Sorry, can't find two minimum circles"
#                return None

#            plotLine(i, ci)
#            plotLine(ci, cf)
#            plotLine(cf, f)

#            return toReturn

        elif type == "MONOCIRCULAR":
#            print "MONOCIRCULAR"
            intersection = getIntersection(i, di, f, df)
            
            if intersection == None:
                if di*df == 1:
                    if di*i > df*f:
                        midpoint = getIntersection(i, di.perp(), f, df)
                        c = (midpoint + i)/2
                        return arc(c, i, midpoint) + Polyline([f], False)     # Check arc direction!!! (removed repeated point?)
                    else:
                        midpoint = getIntersection(i, di, f, df.perp())
                        c = (midpoint + f)/2
                        return Polyline([i], False) + arc(c, midpoint, f)     # Check arc direction!!!
                
                else:
                    print "CIRCULAR would be better for this case because directions are antiparallell; returning linear in the meantime..."
                    return Polyline([i, f], False)

            
            toReturn = Polyline([])
    
            if (intersection - i)*di > 0 and (intersection - f)*df > 0:     # Converging
                if (intersection - i)*di < (intersection - f)*df:
                    midpoint = intersection - df*((intersection - i)*di)
                    c = getIntersection(i, di.perp(), midpoint, df.perp())  # Check if intersection exists for all of these...
                
                    return arc(c, i, midpoint) + Polyline([f], False)
                else:
                    midpoint = intersection - di*((intersection - f)*df)
                    c = getIntersection(midpoint, di.perp(), f, df.perp())

                    return Polyline([i], False) + arc(c, midpoint, f)
            elif (intersection - i)*di > 0 or (intersection - f)*df > 0:    # Opposite
                if (i - intersection)*di < 0:
                    midpoint = intersection - di*((intersection - f)*df)
                    c = getIntersection(midpoint, di.perp(), f, df.perp())
                    
                    return Polyline([i], False) + arc(c, midpoint, f, False)
                else:
                    midpoint = intersection - df*((intersection - i)*di)
                    c = getIntersection(i, di.perp(), midpoint, df.perp())
                    
                    return arc(c, i, midpoint, False) + Polyline([f], False)
            else:                                                           # Diverging
                if (intersection - i)*di > (intersection - f)*df:               # If i is shorter
                    midpoint = intersection - di*((intersection - f)*df)
                    c = getIntersection(midpoint, di.perp(), f, df.perp())
                    
                    print c
                    
                    if c.norm2() < 1e6:
#                        return Polyline([i, midpoint, c, f], False) #arc(c, i, midpoint, False) + Polyline([f], False)
#                        return arc(c, i, midpoint, False) + Polyline([f], False)
                        return Polyline([i], False) + arc(c, midpoint, f, False)
                else:
                    midpoint = intersection - df*((intersection - i)*di)
                    c = getIntersection(i, di.perp(), midpoint, df.perp())
                    
                    print c
                    if c.norm2() < 1e6:
#                        return Polyline([i, c, midpoint, f], False) #+ arc(c, midpoint, f, False)
#                        return Polyline([i], False) + arc(c, midpoint, f, False)
                        return arc(c, i, midpoint, False) + Polyline([f], False)


#            if (c - i).norm2() < (c - f).norm2():
#                if (c - i) * di == 0:
#                    print "CIRCULAR would be better for this case; returning linear in the meantime..."
#                    return Polyline([i, f], False)
#                elif (c - i) * di > 0 and (f - c) * df > 0:
#                    midpoint = c - df*( (c-i).norm() )
#                
#                    toReturn.add(arc(c, i, midpoint))
#                    toReturn.add(f)
#                elif (c - i) * di < 0 and (f - c) * df < 0:
#                    midpoint = c - df*( (c-i).norm() )
#                    
#                    toReturn.add(arc(c, i, midpoint))
#                    toReturn.add(f)

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
        df = -df
    else:
        polyline = polyline_
        di = None
        df = None

    if not isinstance(polyline, Polyline):
        print "No polyline given to thicken..."
        return None
    
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
        i = 1
        while i < polyline.size:       # Check here...
            segmentLength2 = (polyline.points[i] - polyline.points[i-1]).norm2()
            if segmentLength2 > 4*precision*precision:
                print "Length short, adding linear"
                addition = linear(polyline.points[i-1], polyline.points[i])
                polyline.points = polyline.points[0:i-1] + addition.points + polyline.points[i+1:]
                polyline.size = len(polyline.points)
            i += 1

#    polyline.plot()
#    return

    toReturn = Polyline([], True)

#    return toReturn

    p0 = polyline.perp(0, filletType, calcWidth(0, widthType, widthParams), di)
    
    for i in range(1, polyline.size - 1):
        currentLength += (polyline.points[i] - polyline.points[i-1]).norm()
        t = currentLength/length
#        print t, calcWidth(t, widthType, widthParams), (polyline.points[i] - polyline.points[i-1])
        toReturn.add(polyline.perp(i, filletType, calcWidth(t, widthType, widthParams)))
    
    p1 = polyline.perp(polyline.size - 1, filletType, calcWidth(1, widthType, widthParams), df)
    p2 = polyline.perp(polyline.size - 1, filletType, -calcWidth(1, widthType, widthParams), df)

    if capType == 0:
        toReturn.add(p1)
        toReturn.add(p2)
    elif capType == 1:
        toReturn.add(arc((p1+p2)/2, p1, p2))
    
    for i in range(polyline.size - 2, 0, -1):
        currentLength -= (polyline.points[i] - polyline.points[i-1]).norm()
        t = currentLength/length
#        print t, calcWidth(t, widthType, widthParams)
        toReturn.add(polyline.perp(i, filletType, -calcWidth(t, widthType, widthParams)))

    p3 = polyline.perp(0, filletType, -calcWidth(0, widthType, widthParams), di)


    if capType == 0:
        toReturn.add(p3)
        toReturn.add(p0)
    elif capType == 1:
        toReturn.add(arc((p0+p3)/2, p3, p0))

#    print toReturn
    return toReturn


def connectAndThicken(i, f, type="CIRCULAR", widthType="CUBIC", capType="FLAT"):
#    if isinstance(connect(i, f, type), Polyline):
#        connect(i, f, type).plot()
#    print thickenPolyline([connect(i, f, type), i.dir, f.dir], widthType, [i.wid, f.wid], "SHARP", capType)
    return thickenPolyline([connect(i, f, type), i.dir, f.dir], widthType, [i.wid, f.wid], "SHARP", capType)

def circle(c, r, p=precision):
    if r < p:
        steps = 8
    else:
        steps = int(math.ceil(2*math.pi*r/p))
    
    toReturn = Polyline([], True)

    v = Vector(r,0)
    m = Matrix(2*math.pi/steps)
    
    for i in range(0,steps):
        v *= m
        toReturn.add(c + v)

#    print toReturn
    return toReturn

def rect(a, b):
    return Polyline([a, a + Vector(0,b.y - a.y), b, a + Vector(b.x - a.x, 0)], True)

def getArcAng(c, i, f, chooseShortest=True):
    r1 = (i - c).norm()
    r2 = (f - c).norm()
    
    #    print r1 - r2
    
    if r1 - r2 > 1e-6:  # Arbitrary!
        print "Can't make an arc with two radii: " + str(r1) + " and " + str(r2)
        return 1e22  # Arbitrary!
    if (f - i).norm2() < 1e-6:  # Arbitrary!
        print "Start and end of arc at same place..."
        return 0
    
    dir = (i - c).cross(f - c)

    if dir == 0:
        dir = 1
        print "Arcs are equidistant, choosing CCW as shortest"

    ang = dir*math.acos(((i - c).Unit()) * ((f - c).Unit()))

    if not chooseShortest:
        if ang > 0:
            ang = ang - 2*math.pi
        else:
            ang = 2*math.pi + ang
    
    return ang

def arc(c, i, f, chooseShortest=True, p=precision):   # 'direction' : CCW=1, CW=-1, Shortest=0
    r1 = (i - c).norm()
    r2 = (f - c).norm()
    
#    print r1 - r2

    if r1 - r2 > 1e-6:  # Arbitrary!
        print "Can't make an arc with two radii: " + str(r1) + " and " + str(r2)
        return Polyline([], False)
    if (f - i).norm2() < 1e-6:  # Arbitrary!
        print "Start and end of arc at same place..."
        return Polyline([], False)
    
    r = r1

    print (i - c), (f - c)

    dir = (i - c).cross(f - c)

    print "Dir: ", dir

    if dir == 0:
#        dir = 1
        ang = -math.pi
        chooseShortest=True
        print "Arcs are equidistant, choosing CCW as shortest"
    else:
        ang = dir*math.acos(((i - c).Unit()) * ((f - c).Unit()))

#    print (i - c).Unit()
#    print (f - c).Unit()


    if not chooseShortest:
        if ang > 0:
            ang = ang - 2*math.pi
        else:
            ang = 2*math.pi + ang

    if r < p:
        steps = 8
    elif r > 1000:          # Arbitrary, check this....
        return Polyline([], False)
    else:
        steps = int(math.ceil(abs(ang)*r/p))

#    print steps, ang, r, p

    toReturn = Polyline([], False)
    
    if steps > 0:
        v = (i - c)
        print ang/steps
        m = Matrix(ang/steps)
            
        toReturn.add(i)

        for i in range(0,steps-1):
            v *= m
            #        print center + v
            toReturn.add(c + v)

        toReturn.add(f)

#    print toReturn
    return toReturn



