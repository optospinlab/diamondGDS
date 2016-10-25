import math
from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect, connectAndThicken
from geometry import Matrix, Vector, Polyline, getIntersection, Connection
from loading import GDSinfo, TTF
from example_components import gratingMike

import matplotlib.pyplot as plt

#font = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/fish.ttf")
font = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/courier-bold.ttf")

def dev2D(tip=2, tipwid=2, diskspacing=12, electspacing=5, gap=6, groundoffset=2.5, electwid=8, wirewid=6, wirespaceF=10, wirewidF=10, gespace=40, padsize=100, disks=[1.2, 1.3, 1.4, 1.5], couplinggap=.08, couplingwid=.12, couplinglen=1, lrpad=0):
    toReturn = Shape([]);
    
    if diskspacing < electwid:
        return None
    
    numdisks = len(disks)

    electspacing = diskspacing/3.
    groundoffset = diskspacing/4.
    electwid = 2*diskspacing/3.
    wirewid = diskspacing/2.
    wirespace = diskspacing/2.
    gespace = 4.5*electwid
    
    if wirespace >= wirespaceF:
        wirespaceF = wirespace #+.001
    if wirewid >= wirewidF:
        wirewidF = wirewid #+.001
    
            
    v1 = Vector(math.cos(math.pi/2.+couplinglen/2.), math.sin(math.pi/2.+couplinglen/2.))
    v2 = Vector(math.cos(math.pi/2.-couplinglen/2.), math.sin(math.pi/2.-couplinglen/2.))

    prevConnection = 0
    
    tranlen = .75
    
    disky = wirewidF + wirespaceF/2. + groundoffset
    
    gapStuff = Shape([]);

    for i in range(0, numdisks):
        c = Vector((i+.5-numdisks/2.)*diskspacing, disky)
        gapStuff.add(circle(c, disks[i]/2.).setMaterial(1))

        irad = disks[i]/2. + couplinggap
        orad = disks[i]/2. + couplinggap + couplingwid
        
        iwid = couplingwid
        owid = .24
        mrad = (irad + orad)/2.
        
#        pline = arc(c, c+v1, c+v2)

        pline = arc(c, c+v1*irad, c+v2*irad) + arc(c, c+v2*orad, c+v1*orad)
        pline.closed = True

        gapStuff.add(pline.setMaterial(1))
        left =  thickenPolyline(Polyline([c+v1*mrad, c+v1*mrad+v1.perp()*tranlen]), "CUBIC", [iwid, owid]).setMaterial(1)
        right = thickenPolyline(Polyline([c+v2*mrad, c+v2*mrad+v2.perp().perp().perp()*tranlen]), "CUBIC", [iwid, owid]).setMaterial(1)

        gapStuff.add(left)
        gapStuff.add(right)

#        print 'L: ', left.connections
#        print 'R: ', right.connections

        if not isinstance(prevConnection, Connection):
            firstConnection = Connection(c+v1*mrad+v1.perp()*tranlen, v1.perp(), owid)
        else:
            i = prevConnection
            f = Connection(c+v1*mrad+v1.perp()*tranlen, v1.perp(), owid)
            gapStuff.add(connectAndThicken(i,f).setMaterial(1))
        
        prevConnection = Connection(c+v2*mrad+v2.perp().perp().perp()*tranlen, v2.perp().perp().perp(), owid)
            
    gratingOne = Connection(Vector(-numdisks*diskspacing/2. - diskspacing/2., disky), Vector(1,0), owid)
    gratingTwo = Connection(Vector(-numdisks*diskspacing/2. - diskspacing/2. - 9.5 - 5,    disky - 9.5), Vector(0,-1), owid)
    gratingTwoA = Connection(Vector(-(numdisks+2)*diskspacing/2., wirewidF/6.), Vector(1,0), owid)
    gratingTwoC = Connection(Vector(numdisks*diskspacing/2., wirewidF/6.), Vector(1,0), owid)
    
    gapStuff.add(connectAndThicken(gratingOne,firstConnection).setMaterial(1))
    gapStuff.add(connectAndThicken(gratingTwoC,prevConnection).setMaterial(1))
    gapStuff.add(connectAndThicken(-gratingTwoC,gratingTwoA).setMaterial(1))
    gapStuff.add(connectAndThicken(-gratingTwoA,gratingTwo).setMaterial(1))
    gapStuff.add(gratingMike(gratingOne))
    gapStuff.add(gratingMike(gratingTwo))

#    gapStuff.plot();

#        arc(c, c+v1, c+v2).plot()

    y = gespace/4. # electspacing - groundoffset + electwid/2. -wirewid/2 + tipwid/2.

    for i in range(0, (numdisks+2)/2):
        v = Vector((i-numdisks/2.)*diskspacing, electspacing - groundoffset + electwid/2. + disky)
#        if i == 0:
#            rect1 = rect(v + Vector(0, -wirewid/2. + tipwid/2.), v + Vector(-10, wirewid/2. + tipwid/2.))
#            rect1 = rect(v + Vector(wirewid/2., -wirewid/2. + tipwid/2.), v + Vector(-electwid, wirewidF-wirewid/2. + tipwid/2.))
#        else:
        rect1 = -rect(v + Vector(-wirewid/2., -wirewid/2 + tipwid/2.), v + Vector(wirewid/2, y + wirewidF - (electspacing - groundoffset + electwid/2.)))

        if tip == 0:        # SQUARE
            tipobj = rect(v - Vector(electwid/2., electwid/2.), v + Vector(electwid/2., electwid/2.)).union(-rect1).setMaterial(3)
        elif tip == 1:      # POINTY
            x = electwid/2. - tipwid/2.
            if i == 0:
                pline = Polyline([v, v + Vector(x,-x)])
                
                tipobj = rect1.union(-thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND")).setMaterial(3)
            else:
                pline = Polyline([v + Vector(-x,-x), v, v + Vector(x,-x)])
                
                tipobj = thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND").union(-rect1).setMaterial(3)
        elif tip == 2:      # CIRCLE
            tipobj = circle(v, electwid/2.).union(rect1).setMaterial(3)
        
        if i != (numdisks+2)/2.:
            toReturn.add(tipobj)
    
    
    # Pads
#    v = Vector(-padsize-wirespaceF/2., y + 2*wirespaceF + wirewidF + padsize)   # Right
#    toReturn.add(rect(v, v + Vector(padsize, padsize)))
#    toReturn.add(rect(v + Vector(padsize-wirewidF, -padsize + wirewidF + wirespaceF), v + Vector(padsize, 0)))
#    toReturn.add(rect(Vector((2-numdisks/2.)*diskspacing - wirewid/2., gespace/2. + wirewidF), Vector((2-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + 2*wirewidF + 2*wirespaceF)))
#    toReturn.add(rect(Vector((2-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + 2*wirewidF + 2*wirespaceF), v + Vector(padsize-wirewidF, -padsize + wirewidF + wirespaceF)))

    v = Vector(-padsize-wirespaceF-wirewidF/2., y + wirespaceF + wirewidF + disky)    # L/R (prev Middle)
    toReturn.add(rect(v, v + Vector(padsize, padsize)))
    toReturn.add(rect(Vector((1-numdisks/2.)*diskspacing - wirewid/2., y + disky + wirewidF), Vector((1-numdisks/2.)*diskspacing + wirewid/2., y + disky + wirewidF + wirespaceF)))
    toReturn.add(rect(v + Vector(padsize, 0), Vector((1-numdisks/2.)*diskspacing + wirewid/2., y + disky + 2*wirewidF + wirespaceF)))

    toReturn.add(rect(v - Vector(wirespaceF, wirewidF + wirespaceF), Vector((0-numdisks/2.)*diskspacing - wirewid/2., y + disky + wirewidF)))

#    v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, y)                          # Left
##    toReturn.add(rect(v, v + Vector(padsize, padsize)))
#    toReturn.add(rect(v + Vector(padsize, 0), Vector((-numdisks/2.)*diskspacing - wirewid/2., y + wirewidF)))

#    v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, -groundoffset)                          # Ground Left
##    toReturn.add(rect(v, v + Vector(padsize, -padsize)))
#    toReturn.add(rect(v + Vector(padsize, 0), Vector((-numdisks/2.)*diskspacing - wirewid/2., -groundoffset - wirewidF)))

    toReturn.add(toReturn*Matrix(-1,0,0,1)) # FLIP HORIZ

    #toReturn.add(rect(v - Vector(wirewidF + wirespaceF, wirewidF + wirespaceF), v - Vector(wirespaceF, - padsize - wirewidF - wirespaceF)))
    #toReturn.add(rect(Vector(v.x - (wirewidF + wirespaceF), 0), v - Vector(wirespaceF, - padsize - wirewidF - wirespaceF)))
    toReturn.add(rect(Vector(v.x - (2*wirewidF + wirespaceF), 0), Vector(v.x-wirespaceF, 200)))
    toReturn.add(rect(Vector(7*wirewidF/2. + 3*wirespaceF + padsize, 0), Vector(11*wirewidF/2. + 3*wirespaceF + padsize, 200)))   # Ground line

    toReturn.add(rect(v + Vector(-wirespaceF, padsize + wirespaceF), Vector(-v.x + wirespaceF, v.y + padsize + wirespaceF + wirewidF)))

    toReturn.add(rect(Vector(-wirewidF/2., y + disky + 3*wirespaceF + wirewidF), Vector(wirewidF/2., y + disky + 2*wirespaceF + wirewidF + padsize)))
    toReturn.add(rect(Vector(-wirewid/2., y + disky + wirewidF), Vector(wirewid/2., y + disky + 3*wirespaceF + wirewidF)))
    toReturn.add(tipobj)
    
#    if not (lrpad & 0x01):  # Make left pad
#        v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, y)                          # Left
#        toReturn.add(rect(v, v + Vector(padsize, padsize)))
#        v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, -groundoffset)                          # Ground Left
#        toReturn.add(rect(v, v + Vector(padsize, -padsize)))
#    
#    if not (lrpad & 0x02):  # Make right pad
#        v = Vector(-(-padsize-5*wirespaceF/2.-wirewidF), y)                          # Left
#        toReturn.add(rect(v, v + Vector(padsize, padsize)))
#        v = Vector(-(-padsize-5*wirespaceF/2.-wirewidF), -groundoffset)                          # Ground Left
#        toReturn.add(rect(v, v + Vector(padsize, -padsize)))

    # Ground
    gwid = diskspacing*numdisks/2. + electwid/2.
    gwid2 = diskspacing*numdisks/2. + wirewid/2.
#    toReturn.add(rect(Vector(-gwid, -gespace/2.), Vector(gwid, -groundoffset)).setMaterial(3))
#    toReturn.add(rect(Vector(-gwid2, -gespace/2.-wirewidF), Vector(gwid2, -gespace/2.)).setMaterial(3))
    toReturn.add(rect(Vector(-gwid2, wirespaceF/2.), Vector(gwid2 + wirespaceF, wirewidF + wirespaceF/2.)).setMaterial(3))

    toReturn.add((rect(v - Vector(wirewidF + wirespaceF, wirewidF + wirespaceF), v - Vector(wirespaceF, - padsize - wirewidF - wirespaceF))*Matrix(-1,0,0,1)).setMaterial(3))
    
    toReturn.setMaterial(3)

    toReturn.add(gapStuff)

    toReturn.add(toReturn*Matrix(1,0,0,-1)) # FLIP VERT

    toReturn.add(rect(Vector(gwid2 + wirespaceF, -wirewidF - wirespaceF/2.), Vector(gwid2 + wirespaceF + wirewidF, wirewidF + wirespaceF/2.)).setMaterial(3))
    toReturn.add(rect(Vector(gwid2 + wirespaceF + wirewidF, - wirewidF), Vector(7*wirewidF/2. + 3*wirespaceF + padsize, wirewidF)).setMaterial(3))
#    toReturn.add(rect(Vector(3*wirewidF/2. + 3*wirespaceF + padsize, -wirespaceF/2.), Vector(5*wirewidF/2. + 3*wirespaceF + 2*padsize, -wirespaceF/2. + padsize)).setMaterial(3))

#    toReturn.add((rect(v - Vector(wirewidF + wirespaceF, wirewidF + wirespaceF), v - Vector(wirespaceF, - padsize - wirewidF - wirespaceF))*Matrix(-1,0,0,1)).setMaterial(3))

#    toReturn.add((font.shapeFromStringBoundedCentered("42", -1, 7*5) +      Vector(-85, 0)).setMaterial(3))

#    return [toReturn.setMaterial(3), 2*padsize + 3*wirespaceF + groundoffset + gespace/2. + 3*wirewidF]

    return toReturn

def boundingDiamond(wid=50, inner=1500, owid=250, outer=2250, left="Left", right="Right", center="Center", centeru="?"):
    print "boundingDiamond"
    toReturn = Shape([])
    
    v = Vector(1,1)
    w = Vector(1,-1)
    
    oo = outer/2.
    oi = (outer - owid)/2.
    
#    print outer, wid, outer-wid
#    print oo, oi

    m = (Matrix(1, -1, 1, 1)/math.sqrt(2))

    rect1 = Polyline([v*oo, w*oo, -v*oo, -w*oo, v*oo, v*oi, -w*oi, -v*oi, w*oi, v*oi], True, False, 3)*m;
    
    oo = inner/2.
    oi = (inner - wid)/2.
    rect2 = Polyline([v*oo, w*oo, -v*oo, -w*oo, v*oo, v*oi, -w*oi, -v*oi, w*oi, v*oi], True, False, 3)

    toReturn.add(rect(Vector(-inner/2, -inner/3), Vector(-inner/2 + wid, inner/3)).setMaterial(3))
    toReturn.add(rect(Vector(inner/2, -inner/3), Vector(inner/2 - wid, inner/3)).setMaterial(3))
    if centeru[0] != '?':
        toReturn.add(rect(Vector(-inner/3, inner/2-wid), Vector(inner/3, inner/2)).setMaterial(3))
    toReturn.add(rect(Vector(-inner/3, -inner/2+wid), Vector(inner/3, -inner/2)).setMaterial(3))

#    rect1 = (rect(v*(-oi), v*oi)).add(rect(v*(-oo), v*oo))

#    print rect1

#    toReturn.add(rect(v*(-oi), v*oi));
#    toReturn.add(rect(v*(-oo), v*oo));

    toReturn.add(rect1.setMaterial(3))
#    toReturn.add(rect2)

    toReturn.add((font.shapeFromStringBoundedCentered(left, wid, -1) +      Vector(-inner/2. - inner/4. + 3*wid, 0)).setMaterial(3))
    toReturn.add((font.shapeFromStringBoundedCentered(center, wid, -1) +    Vector(0, -inner/2. - inner/4. + 4*wid)).setMaterial(3))
    toReturn.add((font.shapeFromStringBoundedCentered(right, wid, -1) +      Vector(inner/2. + inner/4. - 3*wid, 0)).setMaterial(3))
    if centeru[0] != '?' and centeru[0] != ' ':
        toReturn.add((font.shapeFromStringBoundedCentered(centeru, wid, -1) +    Vector(0, +inner/2. + inner/4. - 4*wid)).setMaterial(3))

    mark = alignmentMark(100).setMaterial(3)*m;
    
    mx = inner - 5*wid;
    
    toReturn.add(mark + Vector(0, mx));
    toReturn.add(mark + Vector(0, -mx));
    toReturn.add(mark + Vector(mx, 0));
    toReturn.add(mark + Vector(-mx, 0));
    
    return toReturn

def alignmentMark(wid=50):
    toReturn = Shape([])
    
    w = wid/2.
    x = wid/12.
    
    pline = Polyline([Vector(w, x), Vector(w, 2.5*x), Vector(2.5*x, 2.5*x), Vector(2.5*x, w), Vector(x, w), Vector(x,x)])
    
    m = Matrix(0, 1, -1, 0);
    
    for i in range(0, 4):
        toReturn.add(pline);
        pline *= m
    
    return toReturn

def membrane(boxdim=200, viawid=16, boxnum=7, viagap=75):
    toReturn = Shape([]);
    
    box = rect(Vector(-.5,-.5)*boxdim, Vector(.5,.5)*boxdim)
    
    line = Polyline([Vector(-(boxdim - viagap)/2., boxdim/2.), Vector((boxdim - viagap)/2., boxdim/2.)]);
    
    via = thickenPolyline(line, "LINEAR", viawid/2., "SHARP", "ROUND")
    
    box = box.intersect(via);
    box = box.intersect(via*Matrix(math.pi/2));
    box = box.intersect(via*Matrix(math.pi));
    box = box.intersect(via*Matrix(3*math.pi/2));
    
    #edge = box.intersect(rect(Vector(-boxdim, -boxdim/2.+viagap), Vector(boxdim, boxdim)))
    #r = rect(Vector(-boxdim, -boxdim/2.+viagap), Vector(boxdim, boxdim))
    #edge = box.intersect(r)
    
    for x in range(0, boxnum+2):
        for y in range(0, boxnum+2):
            if   x == 0           and y == 0:
                0
            elif x == boxnum+1    and y == 0:
                0
            elif x == 0           and y == boxnum+1:
                0
            elif x == boxnum+1    and y == boxnum+1:
                0
            elif x == 0:
                0 #toReturn.add(edge + Vector(x,y)*boxdim)
            elif x == boxnum+1:
                0 #toReturn.add(edge + Vector(x,y)*boxdim)
            elif y == 0:
                0 #toReturn.add(edge + Vector(x,y)*boxdim)
            elif y == boxnum+1:
                0 #toReturn.add(edge + Vector(x,y)*boxdim)
            else:
                toReturn.add(box + Vector(x, y)*boxdim)

    #toReturn.setMaterial(4).plot()

    return (toReturn + Vector(-boxdim*(boxnum+1)/2., -boxdim*(boxnum+1)/2.)).setMaterial(4)

def starkDevice():
    return 0

def starkChip(wire=10):
    boxdim = 200
    padsize = 100
    
#    membrane(boxdim).plot()

    toReturn = Shape([]);
    
    dev = dev2D()
    
    box = rect(Vector(0,0), Vector(1,1))
    
    for x in range(0, 4):
        for y in range(0,4):
            text = (font.shapeFromStringBoundedCentered(str(x+1) + str(y+1), -1, 7*5) + Vector(-85, 0)).setMaterial(3)
            text2 = (font.shapeFromStringBoundedCentered(str(x+1) + str(y+1), -1, 5) +   Vector(-35, 0)).setMaterial(1)
            toReturn.add(dev +      Vector(x-1.5, y-1.5)*boxdim*2);
            toReturn.add(text +     Vector(x-1.5, y-1.5)*boxdim*2);
            toReturn.add(text2 +    Vector(x-1.5, y-1.5)*boxdim*2 + Vector(0, 10));
            #toReturn.add(text2 +    Vector(x-1.5, y-1.5)*boxdim*2 + Vector(0, -10));

            for xx in range(0,4):
                for yy in range(0,4):
                    if not (xx == x and yy == y):
                        toReturn.add(box + Vector(2*(xx-2)-35+.5, 2*(yy-2)-10+.5) + Vector(x-1.5, y-1.5)*boxdim*2);


#    for x in range(0, 4):
#        toReturn.add(rect(Vector(0,0), Vector(padsize, padsize)) + Vector((x-2)*boxdim*2 + 40, boxdim*2*2));
#        toReturn.add(rect(Vector(0,0), Vector(padsize, padsize)) + Vector((x-1)*boxdim*2 - padsize, boxdim*2*2));

    return toReturn

def starkRound2(fname):
    gds = GDSinfo()
    
    chip = starkChip()
    
#    chip.plot()

    gds.add(chip)
    gds.add(membrane().setMaterial(4))
    
    gds.exportGDS(fname)
    
    return chip


if __name__ == "__main__":
    example_project("/Users/I/Desktop/Desktop/diamondGDS/gds/test3.gds") #"/Users/I/Desktop/diamondGDS/gds/test3.gds"




