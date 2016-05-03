from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect
from geometry import Vector, Polyline, getIntersection, Connection
from font import TTF
from loading import GDSinfo

import matplotlib.pyplot as plt

def fontTest(string="TrueType"):
#    font1 = TTF("/Users/I/Desktop/diamondGDS/Arial.ttf")
#    font2 = TTF("/Users/I/Desktop/diamondGDS/Pilgiche.ttf")
    font1 = TTF("/Users/I/Desktop/diamondGDS/courier-bold.ttf")
#    font1 = TTF("/Users/I/Desktop/diamondGDS/fish.ttf")

#    dv = Vector(1200,0)/1500.
#    v = Vector(0,1)
#    w = Vector(0,0)
#
#    for char in string:
#        polyline = font1[char]
#        (polyline + v).plot()
#        v += dv
#    
#        polyline = font2[char]
#        (polyline + w).plot()
#        w += dv
    font1.shapeFromString(string).plot()

def intersectionTest():
    c1 = circle(Vector(0,0), 1)
    c2 = circle(Vector(1,1), 1.5)
    
    c1.plot()
    c2.plot()
    
#    (c1.union(c2) + Vector(4,0)).plot()
#    (c2.union(c1) + Vector(8,0)).plot()
#    (c1.union(-c2) + Vector(12,0)).plot()
#    (c2.union(-c1) + Vector(16,0)).plot()

    print rect(Vector(3,3), Vector(6,6))
    print rect(Vector(6,3), Vector(12,6))
    
#    (rect(Vector(3,3), Vector(6,6)).union(rect(Vector(6,3), Vector(12,6))) + Vector(12,0)).plot()
    (rect(Vector(6,2), Vector(12,6)).union(rect(Vector(3,3), Vector(6,7))) + Vector(0,0)).plot()
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
    c0 = Connection(Vector(0,-1), Vector(1,0), .2)
    c1 = Connection(Vector(0,1), Vector(1,0), .3)
    
    curve = connect(c0, c1, curveType)
    
#    print curve

    thickenPolyline(curve, "CUBIC", [.2, 1]).plot()
    
    curve.plot()
    curve.plotPerp()
    print thickenPolyline(curve, "CUBIC", [.2, 1]).area()

def gratingTest():
#    grating(Connection(Vector(0,0), Vector(1,2), .27))
#    grating(Connection(Vector(0,0), Vector(1,1), .27))
#    grating(Connection(Vector(0,0), Vector(2,1), .27))
#    grating(Connection(Vector(0,0), Vector(6,1), .27))
    return grating(Connection(Vector(0,0), Vector(1,0), .27))

def importTest():
    info = GDSinfo()
    info.importGDS("/Users/I/Desktop/diamondGDS/test3.gds")
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
    font1 = TTF("/Users/I/Desktop/diamondGDS/courier-bold.ttf")
    font2 = TTF("/Users/I/Desktop/diamondGDS/fish.ttf")
    font3 = TTF("/Users/I/Desktop/diamondGDS/Arial.ttf")
    
    shape = font1.shapeFromString("Glorious TrueType 1234567890") + Vector(0,4)
    shape2 = font2.shapeFromString("Glorious TrueType 1234567890") + Vector(0,2)
    shape3 = font3.shapeFromString("Glorious TrueType 1234567890")
    
#    print "START!"

    print shape
    
    info.shapes[0] = shape
    info.shapes[1] = shape2
    info.shapes[2] = shape3
    info.shapes[3] = gratingTest()
    shape.plot()
    shape2.plot()
    shape3.plot()
    
    info.exportGDS("/Users/I/Desktop/diamondGDS/test3.gds")

#            i += 1
#
#            if i > 2:
#                break
#                break

fontTest("Glorious TrueType 1234567890")

#intersectionTest()
gratingTest()
#connectionTest("QBEZIER")
#connectionTest("CIRCULAR")
#exportTest2()
#
#importTest()

plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()