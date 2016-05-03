import math
from geometry import Matrix, Vector, Polyline, Connection, getIntersection
from shapes import Shape, precision, printPrecision, circle, arc, qBezier

import fontTools
from fontTools.ttLib import TTFont

import matplotlib.pyplot as plt

####  TTF  #####################################################################################
class TTF: #####################################################################################
    tt = None
    cmap = None
    
    width = 0
    linegap = 0
    
    ##### INITIATION #####======================================================================
    def __init__(self, fname):  # Loads TrueType Font from fname. Returns success
        self.tt = TTFont(fname)
    
#        print self.tt.getGlyphNames()
        self.getCMAP()
    
        print self.tt.keys()
        
        #        print self.tt['head']
        self.width = .8*self.tt['hhea'].advanceWidthMax
        self.linegap = self.tt['hhea'].lineGap
    
        print self.width, self.linegap
#        print self.tt[ 'hdmx' ].hdmx
#        print self.tt[ 'kern' ]
#        
#        print self.tt.tables['kern']

    def __getitem__(self, i):
        if type(i) is str:
            i = ord(i)
        #self.tt.getGlyphNames()[i]
#        print self.getCMAP().cmap[i]
        return self.shapeFromGlyph( self.tt[ 'glyf' ][ self.getCMAP().cmap[i] ] )
            
    def getCMAP(self):
        if self.cmap == None:
            for table in self.tt['cmap'].tables:
                print table
                if isinstance(table, fontTools.ttLib.tables._c_m_a_p.cmap_format_0) or isinstance(table, fontTools.ttLib.tables._c_m_a_p.cmap_format_4):
    #                print table
    #                print table.cmap
    #                print "\n"
    #                print sorted(table.cmap.items())
                    self.cmap = table
                    break
        return self.cmap

    def shapeFromGlyph(self, glyph):    # Save loaded glyphs for speed
        toReturn = Shape([],[])
        
        if glyph.isComposite():
            print "Warning: This case is broken!, it does not transform..."
#            print "COMPOSITE"
            for component in glyph.components:
                print component
                print component.getComponentInfo()
                [name, transform] = component.getComponentInfo()
                print transform
                print type(transform)
                m = Matrix(transform)
                print m
                print self.tt['glyf'][name]
                toReturn.add(self.shapeFromGlyph(self.tt['glyf'][name]))
#                for item in self.getCMAP().cmap.items():
#                    if item[1] == name:
#                        toReturn.add(self.shapeFromGlyph(self.tt[ 'glyf' ][item[0]]))
#                        break
        else:
            
#            print "NOT COMPOSITE"
            last = 0
            for i in range(glyph.numberOfContours):
                toAdd = Polyline([], True)
                prevV = None
                prevOn = None
                prevprevV = None
                prevprevOn = None
                
                firstV = None
                firstOn = None
                secondV = None
                secondOn = None
                for j in range(last, glyph.endPtsOfContours[i] + 1):
                    v = Vector(glyph.coordinates[j][0], glyph.coordinates[j][1])/float(self.width)  # This is a temporary fix!
                    on = glyph.flags[j] & 0x01
                    
                    if firstOn == None:
                        firstOn = on
                        firstV = v
                    elif secondOn == None:
                        secondOn = on
                        secondV = v
                    
#                    print v
#                    print prevprevOn, prevOn, on
#                    print prevprevV, prevV, v

                    if prevOn and on:
                        if prevprevOn == None:
                            toAdd.add(prevV)
                        toAdd.add(v)
                    elif prevOn != None and prevprevOn != None:
                        if prevprevOn and not prevOn:
                            if on:          # 101
                                toAdd.add(qBezier(prevprevV, prevV, v))
                            elif not on:    # 100
#                                print (prevV + v)
#                                print (prevV + v)/2
                                toAdd.add(qBezier(prevprevV, prevV, (prevV + v)/2))
                        elif not prevprevOn and not prevOn:
                            if on:          # 001
                                toAdd.add(qBezier((prevprevV + prevV)/2, prevV, v))
                            elif not on:    # 000
                                toAdd.add(qBezier((prevprevV + prevV)/2, prevV, (prevV + v)/2))
        
                    prevprevOn = prevOn
                    prevprevV = prevV
                    prevOn = on
                    prevV = v
#                    print "toAdd: "
#                    print toAdd
#                    print "First Here"
#                    print prevOn, on, firstOn
#                    print prevprevV, v, firstV

#                toAdd.add(Vector(0,0))

                if not on:
                    if firstOn != None and not firstOn:
                        if prevprevOn:
                            toAdd.add(qBezier(prevprevV, v, (v + firstV)/2))
                        else:
                            toAdd.add(qBezier((prevprevV + v)/2, v, (v + firstV)/2))
                    if firstOn != None and firstOn:
                        if prevprevOn:
                            toAdd.add(qBezier(prevprevV, v, firstV))
                        else:
                            toAdd.add(qBezier((prevprevV + v)/2, v, firstV))
                
#                if firstOn != None and secondOn != None:
#                    print "First Second Here"
#                    print on, firstOn, secondOn
##                    if on and firstOn and secondOn:                # 111
#                    if on and not firstOn and secondOn:             # 101
#                        toAdd.add(qBezier(v, firstV, secondV))
#                    if on and not firstOn and not secondOn:         # 100
#                        toAdd.add(qBezier(v, firstV, (firstV + secondV)/2))
#                    if not on and not firstOn and secondOn:         # 001
#                        toAdd.add(qBezier((v + firstV)/2, firstV, secondV))
#                    if not on and not firstOn and not secondOn:     # 000
#                        toAdd.add(qBezier((v + firstV)/2, firstV, (firstV + secondV)/2))

#                toAdd.add(v)
                last = glyph.endPtsOfContours[i] + 1
#                print toAdd.area()
#                toAdd.add(Vector(0,0))
                toReturn.add(toAdd)
#                print "toReturn: "
#                print toReturn

            if len(toReturn.polylines) > 1:
                k = 0

                for i in range(0, toReturn.size):
#                    print toReturn.polylines[i].area()
                    if abs(toReturn.polylines[i].area()) > abs(toReturn.polylines[k].area()):   # Save area for speed
                        k = i
            
                finList = []
                
                for i in range(0, toReturn.size):
                    if toReturn.polylines[i].area() < 0:
#                        print k, i
#                        print toReturn.polylines[i]

#                        print toReturn.polylines[k]

#                        toReturn.polylines[i].points.reverse()

                        m = 0 #toReturn.polylines[i].size-1

                        j = 0
                        norm = (toReturn.polylines[k].points[0] - toReturn.polylines[i].points[m]).norm2()    # Possible error if empty
                        
                        toReturn.polylines[k].sizeCalc()
                        
                        for l in range(0, toReturn.polylines[k].size):
#                            print norm, (toReturn.polylines[k].points[l] - toReturn.polylines[i].points[m]).norm2()
                            if (toReturn.polylines[k].points[l] - toReturn.polylines[i].points[m]).norm2() < norm:
                                j = l
                                norm = (toReturn.polylines[k].points[l] - toReturn.polylines[i].points[m]).norm2()
                    
#                        print j
# toReturn.polylines[k].points[j],
                        toReturn.polylines[k].points = toReturn.polylines[k].points[0:j+1] + toReturn.polylines[i].points + [toReturn.polylines[i].points[0]] +  toReturn.polylines[k].points[j:]
#                        toReturn.polylines[k].points = toReturn.polylines[k].points[0:j+1] + [toReturn.polylines[i].points[toReturn.polylines[i].size-1]] + toReturn.polylines[i].points + toReturn.polylines[k].points[j:]
                        toReturn.polylines[k].sizeCalc()
                    else:
                        finList += [ toReturn.polylines[i] ]
                            
                toReturn = Shape(finList)
#                        toReturn.polylines.remove(i)
#                finList = [toReturn.polylines[k]]
#        
#                for polyline in toReturn.polylines:
#                    print polyline
#                    if polyline != toReturn.polylines[k]:
#                        print polyline.area()
#                        if polyline.area() < 0:
#                    
#                            highest = polyline.points[0]
#                            print "HIGHEST: ", highest
#                            j = 0
#                            
#                            for i in range(0, polyline.size):
#                                if polyline.points[i].y > highest.y:
#                                    highest = polyline.points[i]
#                                    j = i
#                    
#                            polyline.points.insert(i, highest)
#                            polyline.points.insert(i, highest + Vector(0,2))
#                            polyline.points.insert(i, highest)
#                    
#                        else:
#                            print "extended"
#                            finList.extend(polyline)
#                    
#                    toReturn.polylines[k].union(polyline)
#
#                return Shape(finList,[])

        return toReturn

    def shapeFromString(self, string):
        toReturn = Shape([],[])
#        dv = Vector(1. + self.linegap/self.width,0)
        v = Vector(0,1)
        w = Vector(0,0)
        
        for char in string:
            letter = self[char]
            bb = letter.getBoundingBox()
            if bb != None:
                wid = bb[1].x - bb[0].x
                hgt = bb[1].y - bb[0].y
                shift = bb[0].x
            else:
                wid = 1
                hgt = 1
                shift = 0
            
#            plt.plot([v.x, v.x, v.x + wid, v.x + wid, v.x], [v.y, v.y + hgt, v.y + hgt, v.y, v.y])

#            toReturn.polylines.extend( [(letter + v - Vector(shift, 0))] )
            for polyline in letter.polylines:
                toReturn.polylines.extend( [(polyline + v - Vector(shift, 0))] )
#            polyline = self[char]
#            (polyline + v).plot()
            v += Vector(wid + .2, 0)
#            
#            polyline = font2[char]
#            (polyline + w).plot()
#            w += dv

        toReturn.sizeCalc()
        
        return toReturn



