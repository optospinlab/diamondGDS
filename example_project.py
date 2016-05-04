from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect, connectAndThicken
from geometry import Vector, Polyline, getIntersection, Connection
from loading import GDSinfo, TTF
from example_components import gratingMike

import matplotlib.pyplot as plt

font = TTF("/Users/I/Desktop/diamondGDS/fonts/courier-bold.ttf")

def example_device(g1, g2, string):
    toReturn = Shape([]);
    toReturn.add(gratingMike(g1))
    toReturn.add(gratingMike(g2))
    toReturn.add(connectAndThicken(g1, g2, "MONOCIRCULAR"))
    toReturn.add(font.shapeFromStringBoundedCentered(string, w=0, h=2) + Vector(10,10))

    return toReturn

def example_project(fname):
#    font2 = TTF("/Users/I/Desktop/diamondGDS/fonts/fish.ttf")
#    font3 = TTF("/Users/I/Desktop/diamondGDS/fonts/Arial.ttf")

    gds = GDSinfo()
    
    vertical = Connection(Vector(0,0), Vector(0,-1), .27)
    horizontal = Connection(Vector(10,5), Vector(-1,0), .27)
    
#    vertical.plot()
#    horizontal.plot()

#    gds.add(gratingMike(vertical))
#    gds.add(gratingMike(horizontal))
#    gds.add(connectAndThicken(vertical, horizontal, "CIRCULAR"))
#    gds.add(font.shapeFromStringBoundedCentered("01", w=0, h=2) + Vector(10,10))

    gds.add(example_device(vertical, horizontal, "01"))
    gds.add(example_device(horizontal, vertical, "02") + Vector(15,0))

    gds.plot()
#    gds.exportGDS(fname)

if __name__ == "__main__":
    example_project("/Users/I/Desktop/diamondGDS/gds/test3.gds") #"/Users/I/Desktop/diamondGDS/gds/test3.gds"