import math

from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect, connectAndThicken
from geometry import Vector, Polyline, getIntersection, Connection
from loading import GDSinfo, TTF
from example_project import example_project
from stark import starkRound1

import matplotlib.pyplot as plt

def fontTest(string="TrueType"):
    font1 = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/courier-bold.ttf")
    font1.shapeFromString(string).plot()

def fontIntersectTest(string="T"):
    font1 = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/courier-bold.ttf")
    rect2 = -rect(Vector(-100,-10), Vector(100,10));
    
    font2 = font1.shapeFromStringBoundedCentered(string, -1, 15)

    font2.intersect(-rect2).plot();
#    font2.plot()

def intersectionTest():
    c1 = -circle(Vector(0,0), 1)
    c2 = -circle(Vector(1,1), 1.5)
    c3 = -circle(Vector(0,0), .5)
    r1 = rect(Vector(-1,-1), Vector(1,1))
    
#    print c1.area()
#    print c2.area()
#    print c3.area()
#    
#    c1.plot()
#    c2.plot()
#    
#    (c1.union(c2) + Vector(4,0)).plot()
#    (c2.union(c1) + Vector(8,0)).plot()
#    (c1.union(-c2) + Vector(12,0)).plot()
#    (c2.union(-c1) + Vector(16,0)).plot()
#    (c3.intersect(c1) + Vector(20,0)).plot()
    (c3.intersect(r1)).plot()

#    print rect(Vector(3,3), Vector(6,6))
#    print rect(Vector(6,3), Vector(12,6))

#    (rect(Vector(3,3), Vector(6,6)).union(rect(Vector(6,3), Vector(12,6))) + Vector(12,0)).plot()
#    (rect(Vector(6,2), Vector(12,6)).union(rect(Vector(3,3), Vector(6,7))) + Vector(0,0)).plot()
    return None

def grating(connection):
    wid = 1.5
    wid2 = 1.5/2
    
    base = Shape([thickenPolyline(Polyline([Vector(0,0), Vector(8,0)], False), "CUBIC", [connection.wid,wid])], [connection])
    
    grates = [.15, .26, .25, .145, .26, .16, .245, .105, .365]
    mB = [[.05, .26, .26, .26], [.1, .225, .22, .21], [.15, .185, .18, .175]]
    spacing = .05
    x = 8
    
    i = 0
    
    for grate in grates:
        if len(mB) > i:
            base.add(rect(Vector(x,        -mB[i][1]/2),
                          Vector(x+spacing, mB[i][1]/2)))
            base.add(rect(Vector(x,         mB[i][1]/2 + mB[i][0]),
                          Vector(x+spacing, mB[i][1]/2 + mB[i][0] + mB[i][2])))
            base.add(rect(Vector(x,         mB[i][1]/2 + mB[i][0] + mB[i][2] + mB[i][0]),
                          Vector(x+spacing, mB[i][1]/2 + mB[i][0] + mB[i][2] + mB[i][0] + mB[i][3])))
            base.add(rect(Vector(x,        -mB[i][1]/2 - mB[i][0] - mB[i][2]),
                          Vector(x+spacing,-mB[i][1]/2 - mB[i][0])))
            base.add(rect(Vector(x,        -mB[i][1]/2 - mB[i][0] - mB[i][2] - mB[i][0] - mB[i][3]),
                          Vector(x+spacing,-mB[i][1]/2 - mB[i][0] - mB[i][2] - mB[i][0])))
    
        i += 1
        x += spacing
        base.add(rect(Vector(x, -wid2), Vector(x+grate, wid2)))
        x += grate
    
    base *= connection.matrix()
    base.plot()

    return base

def connectionTest(curveType):
#    c0 = Connection(Vector(-1,-1), Vector(1,0), .2)
#    c1 = Connection(Vector(1,1), Vector(-1,1), .3)
    c0 = Connection(Vector(1,-1), Vector(1,0), .2)
    c1 = Connection(Vector(0,1), Vector(1,0), .3)
    
    curve = connect(c0, c1, curveType)
    
#    print curve

    shape = thickenPolyline([curve, c0.dir, c1.dir], "CUBIC", [.2, 1])
    
    shape.plot()
    
    curve.plot()
    curve.plotPerp()
    print shape.area()
    
    c0.plot()
    c1.plot()

def gratingTest():
#    grating(Connection(Vector(0,0), Vector(1,2), .27))
#    grating(Connection(Vector(0,0), Vector(1,1), .27))
#    grating(Connection(Vector(0,0), Vector(2,1), .27))
#    grating(Connection(Vector(0,0), Vector(6,1), .27))
    return grating(Connection(Vector(0,0), Vector(1,0), .27))

def importTest():
    info = GDSinfo()
    info.importGDS("/Users/I/Desktop/Desktop/diamondGDS/test3.gds")
#    info.importGDS("/Users/I/Desktop/diamondGDS/test2.gds")

#    print info.shapes

#    print info.shapes

    i = 0

    for key in info.shapes:
        for polyline in info.shapes[key].polylines:
            polyline.plot()

def exportTest():
    info = GDSinfo()
    
    info.shapes[0] = gratingTest()
    
    info.exportGDS("/Users/I/Desktop/diamondGDS/test3.gds")

def exportTest2():
    info = GDSinfo()
    font1 = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/courier-bold.ttf")
    font2 = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/fish.ttf")
    font3 = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/Arial.ttf")
    
    shape = font1.shapeFromString("Glorious TrueType 1234567890") + Vector(0,4)
    shape2 = font2.shapeFromString("Glorious TrueType 1234567890") + Vector(0,2)
    shape3 = font3.shapeFromString("Glorious TrueType 1234567890")
    
#    print "START!"

    print shape
    
#    info.shapes[0] = shape
#    info.shapes[1] = shape2
#    info.shapes[2] = shape3
#    info.shapes[3] = gratingTest()
    shape.plot()
    shape2.plot()
    shape3.plot()
    
#    info.exportGDS("/Users/I/Desktop/diamondGDS/test3.gds")

def largeArray(n=8, d=10, wid=.27, kinds=["LINEAR", "QBEZIER", "CBEZIER", "CIRCULAR", "MONOCIRCULAR"]):
    font = TTF("/Users/I/Desktop/diamondGDS/fonts/VeraMono.ttf")
#    font = TTF("/Users/I/Desktop/diamondGDS/fonts/courier-bold.ttf")

    toReturn = Shape([])
    
    v = Vector(0,0)
    dv = Vector(n*d*2)
    
    basedir = Vector(0,1)
    
    c0 = Connection(v.copy(), -basedir.copy(), wid)
    c1 = Connection(v.copy(), basedir.copy(), wid)
    
#    c0.dir = basedir
#    
#    c0.wid = wid
#    c1.wid = wid
#    
    for kind in kinds:
        
        for i in range(0,n+1):
            c1.v = basedir.rotate(i*math.pi/n)*(d)
            
            for j in range(0,2*n):
                print "\n0x" + ("%X" % i) + ("%X" % j)
                
                c1.dir = basedir.rotate(j*math.pi/n)
                
#                print c0, c1

#                (c0 + Vector(d*i*1.5, d*j*1.5) + v).plot()
#                (c1 + Vector(d*i*1.5, d*j*1.5) + v).plot()

                polyline = connectAndThicken(c0, c1, kind)

                if isinstance(polyline, Polyline):
                    toReturn.add(polyline + (Vector(d*i*1.5, d*j*1.5) + v))
                    toReturn.add(font.shapeFromStringBoundedCentered(("%X" % i) + ("%X" % j), w=0, h=2) + (Vector(d*i*1.5, d*j*1.5) + v + Vector(3,3)))
    
        toReturn.add(font.shapeFromStringBoundedCentered(kind, w=0, h=10) + (Vector(d*n*.75, -25) + v))
        
        v += dv

    return toReturn

#def largeArrayTest():


#            i += 1
#
#            if i > 2:
#                break
#                break

#fontTest("Glorious TrueType 1234567890")

#intersectionTest()
#gratingTest()
#connectionTest("QBEZIER")
#connectionTest("CIRCULAR")
#exportTest2()
#
#importTest()

#example_project("/Users/I/Desktop/diamondGDS/gds/test3.gds")

#largeArray(8, 10, .27, ["MONOCIRCULAR"]).plot() #"CBEZIER", "QBEZIER", "CIRCULAR", "MONOCIRCULAR"


#fontIntersectTest()

starkRound1("/Users/I/Desktop/Desktop/diamondGDS/gds/test3.gds")

plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()