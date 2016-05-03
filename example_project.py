from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect, connectAndThicken
from geometry import Vector, Polyline, getIntersection, Connection
from loading import GDSinfo, TTF
from example_device import gratingMike

import matplotlib.pyplot as plt

def example_project(fname):
    gds = GDSinfo()
    
    vertical = Connection(Vector(0,0), Vector(0,-1), .27)
    horizontal = Connection(Vector(10,5), Vector(-1,0), .27)
    
#    vertical.plot()
#    horizontal.plot()

    gds.add(gratingMike(vertical))
    gds.add(gratingMike(horizontal))
    gds.add(connectAndThicken(vertical, horizontal, "CBEZIER"))

    gds.plot()
#    gds.exportGDS(fname)

if __name__ == "__main__":
    example_project("/Users/I/Desktop/diamondGDS/gds/test3.gds") #"/Users/I/Desktop/diamondGDS/gds/test3.gds"