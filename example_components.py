from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect
from geometry import Vector, Polyline, getIntersection, Connection, materials
from loading import GDSinfo, TTF
import matplotlib.pyplot as plt

def gratingMike(connection):
    wid = 1.5
    wid2 = 1.5/2
    
    base = Shape([thickenPolyline(Polyline([Vector(0,0), Vector(8,0)], False), "CUBIC", [connection.wid,wid])], [connection])
    
    grates = [.15, .26, .25, .145, .26, .16, .245, .105, .365]
    spacing = .05
    x = 8
    
    i = 0
    
    mB = [[.05, .26, .26, .26], [.1, .225, .22, .21], [.15, .185, .18, .175]]
    
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
            
#    base = connection.matrix() * base
    base *= connection.matrix()
#    print connection.matrix()

    base.connections += [connection]
#    base.plot()
    connection.plot()
    
    return base






