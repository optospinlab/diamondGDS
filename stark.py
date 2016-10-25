import math
from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect, connect, connectAndThicken
from geometry import Matrix, Vector, Polyline, getIntersection, Connection
from loading import GDSinfo, TTF
from example_components import gratingMike

import matplotlib.pyplot as plt

font = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/fish.ttf")
#font = TTF("/Users/I/Desktop/Desktop/diamondGDS/fonts/courier-bold.ttf")

def capacitor(wirewid=10, wirespace=10, height=1300, width=200, paddepth=100, numY=2., circlewid=5, numcirclesets=4, addBreak=0):
    toReturn = Shape([]);
    
    length = (height - (numY+1)*paddepth)/numY
    
    numcirclesets = int(2*math.sqrt((length-2*wirespace)/(12*circlewid)))

    wire = rect(Vector(0,0), Vector(wirewid, length-2*wirespace))
    wire.material = 3;
    
    d = (length-4.*wirespace)/numcirclesets
#    print length
#    print -4*wirespace
#    print length-4*wirespace
#    print d
#    print ''
#    circlespacing = 1.5*circlewid
#    
##    print range(1,numcirclesets)
#
#    c = circle(Vector(0,0), circlewid/2)
#    x = circlewid/4.
##    c = -rect(Vector(-x,-x), Vector(x,x))
#    c.material = 3;
#    
##    for y in range(0,numcirclesets+1):
##        toReturn.add(circle(Vector(-circlewid, y*d + 2.*wirespace), circlewid/2))
#
#    for y in range(1,numcirclesets+1):
##        print range(0,y)
#
#        for z in range(0,y):
#            print y, z
#            #            circle(Vector(-wirewid/2, (y*d - d/2 + 2*wirespace) - (y*circlespacing/2) + z*circlespacing), circlewid/2).plot()
#            #            wire = (circle(Vector(wirewid/2, (y*d - d/2 + 2*wirespace) - (y*circlespacing/2) + z*circlespacing), circlewid/2)).intersect(wire)
#            wire = (c + Vector(wirewid/2., (y*d - d/2. + 2.*wirespace) - ((y-1)*circlespacing/2.) + z*circlespacing)).intersect(wire)

#    for

#    m = Matrix(math.pi, wirewid, length)
#    
#    print m

    wire2 = wire*Matrix(math.pi, wirewid, length)
    
#    print wire
#    print wire2

    x = 0;
    
    wires = Shape([]);
    
    while x < width - 1*(wirewid):
        wires.add(wire + Vector(x, 0))
        x += wirewid+wirespace
        
        if x < width - 1*(wirewid):
            wires.add(wire2 + Vector(x, 0))
            x += wirewid+wirespace

    pad = rect(Vector(0, 0), Vector(x-wirespace, paddepth));
    pad.material = 3;

    pad2 = rect(Vector(0, addBreak/2. + paddepth/2.), Vector(x-wirespace, paddepth));
    pad3 = rect(Vector(0, 0), Vector(x-wirespace, -addBreak/2. + paddepth/2.));
    pad2.material = 3;
    pad3.material = 3;

    toReturn.add(pad)

    for i in range(0, numY):
        toReturn.add(wires + Vector(0, i*(length + paddepth) + paddepth))
        if i != numY-1 and addBreak:
            toReturn.add(pad2 + Vector(0, (i+1)*(length+paddepth)))
            toReturn.add(pad3 + Vector(0, (i+1)*(length+paddepth)))
        else:
            toReturn.add(pad + Vector(0, (i+1)*(length+paddepth)))
    
    
    
    if x-wirespace < width:
        print 'capacitor: Could not fit another wire in. Shrinking the pad width.'
    
#    toReturn.add(font.shapeFromStringBoundedCentered(string, w=0, h=2) + Vector(10,10))

#    toReturn.plot()

    return [toReturn, x-wirespace]

def dev2D(tip=1, tipwid=2, diskspacing=12, electspacing=5, gap=6, groundoffset=2.5, electwid=8, wirewid=6, wirespaceF=10, wirewidF=10, gespace=40, padsize=100, disks=[1.2, 1.25, 1.3, 1.35, 1.4], couplinggap=.08, couplingwid=.12, couplinglen=1, lrpad=0):
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
    
#    gapStuff = Shape([]);
#
#    for i in range(0, numdisks):
#        c = Vector((i+.5-numdisks/2.)*diskspacing, 0)
#        gapStuff.add(circle(c, disks[i]/2.).setMaterial(1))
#
#        irad = disks[i]/2. + couplinggap
#        orad = disks[i]/2. + couplinggap + couplingwid
#        
#        iwid = couplingwid
#        owid = .24
#        mrad = (irad + orad)/2.
#        
##        pline = arc(c, c+v1, c+v2)
#
#        pline = arc(c, c+v1*irad, c+v2*irad) + arc(c, c+v2*orad, c+v1*orad)
#        pline.closed = True
#
#        gapStuff.add(pline.setMaterial(1))
#        left =  thickenPolyline(Polyline([c+v1*mrad, c+v1*mrad+v1.perp()*tranlen]), "CUBIC", [iwid, owid]).setMaterial(1)
#        right = thickenPolyline(Polyline([c+v2*mrad, c+v2*mrad+v2.perp().perp().perp()*tranlen]), "CUBIC", [iwid, owid]).setMaterial(1)
#
#        gapStuff.add(left)
#        gapStuff.add(right)
#
##        print 'L: ', left.connections
##        print 'R: ', right.connections
#
#        if not isinstance(prevConnection, Connection):
#            firstConnection = Connection(c+v1*mrad+v1.perp()*tranlen, v1.perp(), owid)
#        else:
#            i = prevConnection
#            f = Connection(c+v1*mrad+v1.perp()*tranlen, v1.perp(), owid)
#            gapStuff.add(connectAndThicken(i,f).setMaterial(1))
#        
#        prevConnection = Connection(c+v2*mrad+v2.perp().perp().perp()*tranlen, v2.perp().perp().perp(), owid)
#
#    gapStuff.plot();

#        arc(c, c+v1, c+v2).plot()

    y = gespace/2. # electspacing - groundoffset + electwid/2. -wirewid/2 + tipwid/2.

    for i in range(0, (numdisks+1)/2):
        v = Vector((i-numdisks/2.)*diskspacing, electspacing - groundoffset + electwid/2.)
#        if i == 0:
#            rect1 = rect(v + Vector(0, -wirewid/2. + tipwid/2.), v + Vector(-10, wirewid/2. + tipwid/2.))
#            rect1 = rect(v + Vector(wirewid/2., -wirewid/2. + tipwid/2.), v + Vector(-electwid, wirewidF-wirewid/2. + tipwid/2.))
#        else:
        rect1 = -rect(v + Vector(-wirewid/2., -wirewid/2 + tipwid/2.), v + Vector(wirewid/2, gespace/2. + wirewidF - (electspacing - groundoffset + electwid/2.)))

        if tip == 0:        # SQUARE
            toReturn.add(rect(v - Vector(electwid/2., electwid/2.), v + Vector(electwid/2., electwid/2.)).union(-rect1).setMaterial(3))
        elif tip == 1:      # POINTY
            x = electwid/2. - tipwid/2.
            if i == 0:
                pline = Polyline([v, v + Vector(x,-x)])
                toReturn.add(rect1.union(-thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND")).setMaterial(3))
#                toReturn.add(rect1)
#            elif i == numdisks:
#                pline = Polyline([v + Vector(-x,-x), v])
#                toReturn.add(thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND").setMaterial(3))
            else:
                pline = Polyline([v + Vector(-x,-x), v, v + Vector(x,-x)])
#                pline.plot()
#                toReturn.add(thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND").setMaterial(3))
#                toReturn.add(rect(v + Vector(-wirewid/2., -wirewid/2 + tipwid/2.), v + Vector(wirewid/2, 10)).setMaterial(3))
                toReturn.add(thickenPolyline(pline, "CONSTANT", tipwid/2., "SHARP", "ROUND").union(-rect1).setMaterial(3))
        elif tip == 2:      # CIRCLE
            toReturn.add(circle(v, electwid/2.).union(rect1).setMaterial(3))
    
    # Pads
    v = Vector(-padsize-wirespaceF/2., y + 2*wirespaceF + wirewidF + padsize)   # Right
    toReturn.add(rect(v, v + Vector(padsize, padsize)))
    toReturn.add(rect(v + Vector(padsize-wirewidF, -padsize + wirewidF + wirespaceF), v + Vector(padsize, 0)))
    toReturn.add(rect(Vector((2-numdisks/2.)*diskspacing - wirewid/2., gespace/2. + wirewidF), Vector((2-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + 2*wirewidF + 2*wirespaceF)))
    toReturn.add(rect(Vector((2-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + 2*wirewidF + 2*wirespaceF), v + Vector(padsize-wirewidF, -padsize + wirewidF + wirespaceF)))
    
    v = Vector(-padsize-3*wirespaceF/2.-wirewidF, y + wirespaceF + wirewidF)    # Middle
    toReturn.add(rect(v, v + Vector(padsize, padsize)))
    toReturn.add(rect(Vector((1-numdisks/2.)*diskspacing - wirewid/2., gespace/2. + wirewidF), Vector((1-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + wirewidF + wirespaceF)))
    toReturn.add(rect(v + Vector(padsize, 0), Vector((1-numdisks/2.)*diskspacing + wirewid/2., gespace/2. + 2*wirewidF + wirespaceF)))
    
    v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, y)                          # Left
#    toReturn.add(rect(v, v + Vector(padsize, padsize)))
    toReturn.add(rect(v + Vector(padsize, 0), Vector((-numdisks/2.)*diskspacing - wirewid/2., y + wirewidF)))
    
    v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, -groundoffset)                          # Ground Left
#    toReturn.add(rect(v, v + Vector(padsize, -padsize)))
    toReturn.add(rect(v + Vector(padsize, 0), Vector((-numdisks/2.)*diskspacing - wirewid/2., -groundoffset - wirewidF)))

    toReturn.add(toReturn*Matrix(-1,0,0,1))
    
    if not (lrpad & 0x01):  # Make left pad
        v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, y)                          # Left
        toReturn.add(rect(v, v + Vector(padsize, padsize)))
        v = Vector(-2*padsize-5*wirespaceF/2.-wirewidF, -groundoffset)                          # Ground Left
        toReturn.add(rect(v, v + Vector(padsize, -padsize)))
    
    if not (lrpad & 0x02):  # Make right pad
        v = Vector(-(-padsize-5*wirespaceF/2.-wirewidF), y)                          # Left
        toReturn.add(rect(v, v + Vector(padsize, padsize)))
        v = Vector(-(-padsize-5*wirespaceF/2.-wirewidF), -groundoffset)                          # Ground Left
        toReturn.add(rect(v, v + Vector(padsize, -padsize)))

    # Ground
    gwid = diskspacing*numdisks/2. + electwid/2.
    gwid2 = diskspacing*numdisks/2. + wirewid/2.
#    toReturn.add(rect(Vector(-gwid, -gespace/2.), Vector(gwid, -groundoffset)).setMaterial(3))
#    toReturn.add(rect(Vector(-gwid2, -gespace/2.-wirewidF), Vector(gwid2, -gespace/2.)).setMaterial(3))
    toReturn.add(rect(Vector(-gwid2, -groundoffset-wirewidF), Vector(gwid2, -groundoffset)).setMaterial(3))

    return [toReturn.setMaterial(3), 2*padsize + 3*wirespaceF + groundoffset + gespace/2. + 3*wirewidF]

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

def starkRound1(fname):
    gds = GDSinfo()
    
#    gds.add(capacitor(10, 10, 150, 200, 100, 5, 5, 3, 4));
#    gds.add(dev2D(0) + Vector(0, 100));
#    gds.add(dev2D(1) + Vector(0, 50));

    xi = 0
    yi = 0
    
    P = [75, 100, 150];
    CS = [7, 10, 25] #, 8, 10, 15, 20
    T = [0, 2] #, -7]#, 3]
    N = [2]
    WWS = [10, 15]
    DS = [14, 16, 18, 20, 25, 30]

    for p in P:
        for cs in CS:
            for n in N:
                for wws in WWS:
                    yi += 1;
                    for t in T:
                        for ds in DS:
                            xi += 1;
                            
#                            wws = 10

    #                        print p, cs, t

                            chip = Shape([], []);
                            
                            boxwid = 1400 - 4*wws
                            
                            tipwid = 2
                                
                            if t < 0:
                                tipwid = -t
                                t = 1
                            
                            tipwid *= ds/12.
                            tipwid = int(tipwid*100)/100.
                                
                            if t == 3:
                                [dev, devhgt] = dev2D(T[0], padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30)
                            else:
                                [dev, devhgt] = dev2D(t, padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30)
                            
                            [bbll, bbur] = dev.getBoundingBox()
                            
                            wid = bbur.x - bbll.x;
                            
                            capwid = (boxwid - wid - 4*wws)/2.
                            
                            numcap = int((boxwid/devhgt) + .25)
                            
                            for i in range(1, numcap+1):
                                if t == 3:
                                    if i == 1:
                                        chip.add(dev + Vector(0, -boxwid/2. + (i-1)*devhgt + p + wws*2));
                                    else:
    #                                    print T[i-1]
    #                                    print dev2D(T[i-1], diskspacing=ds, padsize=p, wirewidF=wws, wirespaceF=wws, gespace=30)
                                        t2 = T[i-1]
                                        if t2 < 0:
                                            t = 1
                                            tipwid = -t2

                                        chip.add(dev2D(t2, diskspacing=ds, padsize=p, wirewidF=wws, wirespaceF=wws, gespace=30, tipwid=tipwid) + Vector(0, boxwid/2. - i*devhgt));
                                else:
                                    chip.add(dev + Vector(0, -boxwid/2. + (i-1)*devhgt + p + wws*2));
                            
                            [cap, capwidtrue] = capacitor(wirewid=wws, wirespace=cs, height=boxwid, width=capwid, paddepth=p, numY=n, circlewid=5, numcirclesets=4, addBreak=5)
                            
            #                [bbll, bbur] = cap.getBoundingBox()

            #                capwidtrue

                            chip.add(cap - Vector(boxwid/2., boxwid/2.));
                            chip.add(cap + Vector(boxwid/2. - capwidtrue, -boxwid/2.));

                            height=boxwid
                            paddepth=p
                            numY=n
                            
                            l = int((height - paddepth)/float(numY) - paddepth)
                            
                            if   t == 0:
                                type = "SQUARE"
                            elif t == 1:
                                type = "TIP:" + str(tipwid) + "UM"
                            elif t == 2:
                                type = "CIRCLE"
                            elif t == 3:
                                type = "MIXED"

                            chip.add(boundingDiamond(left="W=10um\nS=" + str(cs) + "um\nP=" + str(p) + "um\nL=" + str(l) + "um", center="T=" + type + "\nDS=" + str(ds) + "um\nP=" + str(p) + "um\n[" + str(xi) + ", " + str(yi) + "]", right="W=10um\nS=" + str(cs) + "um\nP=" + str(p) + "um\nL=" + str(l) + "um"));

                            gds.add(chip*(Matrix(1, -1, 1, 1, xi*2250, yi*2250)/math.sqrt(2)))
                    xi = 0;

    
#    yi += 1;
    xi = 0;

    for p in P:
        yi += 1;
        for t in T:
            for ds in DS:
                xi += 1;
                
                wws = 10
                
                #                        print p, cs, t
                
                chip = Shape([], []);
                
                boxwid = 1400 - 4*wws
                
                tipwid = 2
                
                if t < 0:
                    tipwid = -t
                    t = 1
                
                tipwid *= ds/12.
                tipwid = int(tipwid*100)/100.
                
                lrpad = 2
    
                if t == 3:
                    [dev, devhgt] = dev2D(T[0], padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=2)
                else:
                    [dev, devhgt] = dev2D(t, padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=2)
                
#                dev = dev - Vector(p, 0);

                [bbll, bbur] = dev.getBoundingBox()
                    
                wid = bbur.x - bbll.x;
                
                boxwid2 = boxwid - p - 4*wws

                numcap = int((boxwid/devhgt) + .25)

                numdev = -1
    
                while boxwid2 > 0:
                    boxwid2 -= wid
                    numdev += 1
                
                for x in range(1, numdev+1):
                    
                    for i in range(1, numcap+1):
                        if t == 3:
                            if i == 1:
                                chip.add(dev + Vector((x-(numdev+1)*.5)*wid, (i-1-numcap/2.)*devhgt + p + wws*2));
                            else:
                                #                                    print T[i-1]
                                #                                    print dev2D(T[i-1], diskspacing=ds, padsize=p, wirewidF=wws, wirespaceF=wws, gespace=30)
                                t2 = T[i-1]
                                if t2 < 0:
                                    t = 1
                                    tipwid = -t2
                                
                                chip.add(dev2D(t2, diskspacing=ds, padsize=p, wirewidF=wws, wirespaceF=wws, gespace=30, tipwid=tipwid, lrpad=lrpad) + Vector((x-numdev*.5)*wid, boxwid/2. - i*devhgt));
                        else:
                            print (x-(numdev+1)*.5)
                            chip.add(dev + Vector((x-(numdev+1)*.5)*wid, -boxwid/2. + (i-1)*devhgt + p + wws*2));
                
                    if x+1 == numdev:
                        lrpad = 0
                        if t == 3:
                            [dev, devhgt] = dev2D(T[0], padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=0)
                        else:
                            [dev, devhgt] = dev2D(t, padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=0)
                                
#                        dev += Vector(p, 0)
#                    elif x+1 == numdev-1:
#                        print "Bye...";
#                    else:
#                        lrpad = 3
#                        
#                        if t == 3:
#                            [dev, devhgt] = dev2D(T[0], padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=3)
#                        else:
#                            [dev, devhgt] = dev2D(t, padsize=p, diskspacing=ds, wirewidF=wws, wirespaceF=wws, tipwid=tipwid, gespace=30, lrpad=3)

                if   t == 0:
                    type = "SQUARE"
                elif t == 1:
                    type = "TIP:" + str(tipwid) + "UM"
                elif t == 2:
                    type = "CIRCLE"
                elif t == 3:
                    type = "MIXED"
                        
                string = "[" + str(xi) + ", " + str(yi) + "]"
                
                chip.add(boundingDiamond(left=string, center="T=" + type + "\nDS=" + str(ds) + "um\nP=" + str(p) + "um", right=string));
                
                gds.add(chip*(Matrix(1, -1, 1, 1, xi*2250, yi*2250)/math.sqrt(2)))
        xi = 0;

    yi += 1;
    
    boxwid = 1400 - 4*wws
    
    for xi in range(-2, len(T)*len(DS)-2):
        chip = Shape([], []);
        
        wid = 5*xi + 5
        
        x = -boxwid/2.
        h = -boxwid/2.
        
        if xi <= 0:
            string = "L=.5:1:2:3:...um"
            
            wid = .5
            chip.add(rect(Vector(x,-h), Vector(x+wid, h)).setMaterial(3))
            x += 2*wid;
            chip.add(rect(Vector(x,-h), Vector(x+wid, h)).setMaterial(3))
            x += 2*wid;
            chip.add(rect(Vector(x,-h), Vector(x+wid, h)).setMaterial(3))
            x += 2*wid;
            
            wid = 1
            
            i = 1
            
            while x + wid < boxwid/2.:
                if (wid%5) == 0:
                    chip.add(rect(Vector(x,-.95*h), Vector(x+wid, .95*h)).setMaterial(3))
                else:
                    chip.add(rect(Vector(x,-h), Vector(x+wid, h)).setMaterial(3))
                
                x += 2*wid;
                if (i%3) == 0:
                    wid += 1;

                i += 1;
        else:
            string = "L=" + str(wid) + "um";
            
            while x + wid < boxwid/2.:
                chip.add(rect(Vector(x,-h), Vector(x+wid, h)).setMaterial(3))
                x += 2*wid;
        
        string2 = "[" + str(xi+2) + ", " + str(yi) + "]";
        
        chip.add(boundingDiamond(left=string2, center=string, right=string2, centeru=" "));
        
        gds.add(chip*(Matrix(1, -1, 1, 1, (xi+3)*2250, yi*2250)/math.sqrt(2)))
        gds.add(chip*(Matrix(1, -1, 1, 1, (xi+3)*2250, (yi+1)*2250)/math.sqrt(2)))
        gds.add(chip*(Matrix(1, -1, 1, 1, (xi+3)*2250, (yi+2)*2250)/math.sqrt(2)))
            
    yi += 3;
                    
    for xi in range(0, len(T)*len(DS)):
#        chip = Shape([], []);

        v = Vector(1,1)
        w = Vector(1,-1)
        
        oo = 2250/2.
        oi = (2100 - xi*25)/2.
        
        #    print outer, wid, outer-wid
        #    print oo, oi
        
        rect1 = Polyline([v*oo, w*oo, -v*oo, -w*oo, v*oo, v*oi, -w*oi, -v*oi, w*oi, v*oi], True, False, 3).setMaterial(3);
        
        gds.add(rect1 + Vector((xi+1)*2250, yi*2250))
        
        gds.add((font.shapeFromStringBoundedCentered(str(2100 - xi*25) + "um", 100, -1) + Vector((xi+1)*2250, (yi+.6)*2250)).setMaterial(3))

#    print "Plotting"
#    gds.plot()
    print "Exporting"
    gds.exportGDS(fname)
    print "Done"

if __name__ == "__main__":
    example_project("/Users/I/Desktop/Desktop/diamondGDS/gds/test3.gds") #"/Users/I/Desktop/diamondGDS/gds/test3.gds"




