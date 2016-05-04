# NOTE: This file needs quite a bit of cleanup, but is low-priority at this point...

import math
from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect
from geometry import Matrix, Vector, Polyline, getIntersection, Connection, materials
import sys, os, struct, datetime

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
            
    def shapeFromStringBoundedCentered(self, string, w=0, h=0):
        shape = self.shapeFromString(string)
        
        [bbll, bbur] = shape.getBoundingBox()
        c = (bbll + bbur)/2
        
        if w < 0 and h < 0:
            return shape - c
        elif w < 0:
            w = h
        elif h < 0:
            h = w
        
        sw = (bbur-bbll).x
        sh = (bbur-bbll).y
        
        if sw < 0 or sh < 0:
            print "something went horribly wrong..."
        
        ratioShape = sw/sh
        ratioBound = w/h
        
        if ratioBound > ratioShape:
            return (shape - c)*(w/sw)
        elif ratioBound <= ratioShape:
            return (shape - c)*(h/sh)


####  GDStime  ################################################################################
class GDStime: ################################################################################
    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    second = 0
    
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
    
    def set(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
    
    def setCurrent():
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __repr__(self):
        return "Y:" + str(self.year) + " M:" + str(self.month) + " D:" + str(self.day) + " h:" + str(self.hour) + " m:" + str(self.minute) + " s:" + str(self.second)


####  GDSinfo  ################################################################################
class GDSinfo: # http://www.cnf.cornell.edu/cnf_spie9.html
    version = 5     # GDS II Version
    
    modificationTime = GDStime()      # Time of last modification
    accessTime = GDStime()            # Time of last access
    
    modificationTimeS = GDStime()     # Time of last modification
    accessTimeS = GDStime()           # Time of last access
    
    databaseUnitUser = .001    # (in user units) CHECK THIS
    databaseUnitMeters = 1e-9
    
    pathWidth = 0
    
    magnificationFactor = 1
    angleDegreesCCW = 0

    shapes = []
#    currentLayer = 0

    def __init__(self):
        return
#        print "Began import"
#        self.importGDS(fname)
#        print "Finished import"

    def importGDS(self, fname):
        self.shapes = []

        f = open(fname, "rb")
            
        val = f.read(4)
        while val:
#            print int(val.encode('hex'), 16), val
            self.interpretToken(val, f)
            val = f.read(4)
        
#        val = f.read(2)
#        while val:
#            print int(val.encode('hex'), 16), val
#            #            self.interprettoken(val, f)
#            val = f.read(2)

        f.close()

    def add(self, other):
        if isinstance(other, Shape):
            self.shapes += [other]
        elif isinstance(other, Polyline):
            self.shapes += [Shape([other])]
        else:
            print "Error, type not understood"
    
    def plot(self):
        for shape in self.shapes:
            shape.plot()
        
#        if layer in self.shapes:
#            for polyline in self.shapes[key].polylines:
#        else:
#            self.shapes[layer] = shape

    def interpretToken(self, token_, f):
        shapesByLayer = {}
        
        print ':'.join(x.encode('hex') for x in token_)
        length =    int(token_[0:2].encode('hex'), 16)
        token =    int(token_[2].encode('hex'), 16)   # Rename as token
        dataType =  int(token_[3].encode('hex'), 16)
        
        DEBUG = True
        
        if DEBUG: print "LENGTH: " + str(length) + "\t" + hex(token) + "  \t"
        
#        if (dataType == 0 and length != 0) or (dataType == 2 and length != 2) or (dataType == 3 and length != 4) or (dataType == 5 and length != 8):
#            print "Possible error; unexpected length"

        if   token == 0x00: #02:
            if DEBUG: print "HEADER"
            if length != 6: print "Possible error; unexpected length"
#            self.version =  read(f.read(2))
            self.version = struct.unpack(">h", f.read(2))[0]
            print self.version
        elif token == 0x01: #02:
            if DEBUG: print "BGNLIB"
            
            vals = struct.unpack(">hhhhhhhhhhhh", f.read(24))
            
#            self.modificationTime.year =    vals[0]
#            self.modificationTime.month =   vals[1]
#            self.modificationTime.day =     vals[2]
#            self.modificationTime.hour =    vals[3]
#            self.modificationTime.minute =  vals[4]
#            self.modificationTime.second =  vals[5]
#            
#            self.accessTime.year =    vals[6]
#            self.accessTime.month =   vals[7]
#            self.accessTime.day =     vals[8]
#            self.accessTime.hour =    vals[9]
#            self.accessTime.minute =  vals[10]
#            self.accessTime.second =  vals[11]

            self.modificationTime.set(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
            self.accessTime.set(vals[6], vals[7], vals[8], vals[9], vals[10], vals[11])

#            self.modificationTime.set(read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)))
#            self.accessTime.set(read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)), read(f.read(2)))

            print self.modificationTime
            print self.accessTime
        elif token == 0x02: #06:
            if DEBUG: print "LIBNAME"
            string = f.read(length - 4) # Error check this...
            print "Library Name: " + string
        elif token == 0x03: #05:
            if DEBUG: print "UNITS"
            
#            databaseUnitUser = read(f.read(8)) # Fix encoding
#            databaseUnitMeters = read(f.read(8))

            data1 = f.read(8)
            data2 = f.read(8)
            
            print data1, ' '.join(format(ord(x), 'b') for x in data1)
            print data2, ' '.join(format(ord(x), 'b') for x in data2)
            
            databaseUnitUser = read(data1) # Fix encoding
            databaseUnitMeters = read(data2)
            
            if DEBUG:
                print databaseUnitUser
                print databaseUnitMeters
        elif token == 0x04: #00:
            if DEBUG: print "ENDLIB"
        elif token == 0x05: #02:
            if DEBUG: print "BGNSTR"
            
#            self.modificationTimeS.set(int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16))
#            
#            self.accessTimeS.set(int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16), int(f.read(2).encode('hex'), 16))

            vals = struct.unpack(">hhhhhhhhhhhh", f.read(24))
            self.modificationTimeS.set(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
            self.accessTimeS.set(vals[6], vals[7], vals[8], vals[9], vals[10], vals[11])
            
#            self.modificationTimeS.year =    vals[0]
#            self.modificationTimeS.month =   vals[1]
#            self.modificationTimeS.day =     vals[2]
#            self.modificationTimeS.hour =    vals[3]
#            self.modificationTimeS.minute =  vals[4]
#            self.modificationTimeS.second =  vals[5]
#            
#            self.accessTimeS.year =    vals[6]
#            self.accessTimeS.month =   vals[7]
#            self.accessTimeS.day =     vals[8]
#            self.accessTimeS.hour =    vals[9]
#            self.accessTimeS.minute =  vals[10]
#            self.accessTimeS.second =  vals[11]

            print self.modificationTimeS
            print self.accessTimeS
        elif token == 0x06: #06:
            if DEBUG: print "STRNAME"
            
            string = f.read(length - 4) # Error check this...
            print "Structure Name: " + string
        elif token == 0x07: #00:
            if DEBUG: print "ENDSTR"
        elif token == 0x08: #00:
            if DEBUG: print "BOUNDARY"
        elif token == 0x09: #00:
            if DEBUG: print "PATH"
        elif token == 0x0A: #00:
            if DEBUG: print "SREF"
        elif token == 0x0B: #00:
            if DEBUG: print "AREF"
        elif token == 0x0C: #00:
            if DEBUG: print "TEXT"
        elif token == 0x0D: #02:
            self.currentLayer = struct.unpack(">h", f.read(2))[0]
#            self.currentLayer = read(f.read(2))
            if DEBUG:
                print "LAYER"
                print self.currentLayer
        elif token == 0x0F: #03:
            if DEBUG: print "WIDTH"
            pathWidth = struct.unpack(">h", f.read(2))[0]
        elif token == 0x10: #03:
            if DEBUG: print "XY"

            polyline = Polyline([], True, False, self.currentLayer)

            length -= 4
            
            while length > 0:
                length -= 8
                
                v = Vector(struct.unpack(">i", f.read(4))[0]*self.databaseUnitUser, struct.unpack(">i", f.read(4))[0]*self.databaseUnitUser)
#                v = Vector(int(f.read(4).encode('hex'), 16), int(f.read(4).encode('hex'), 16))
#                v = Vector(read(f.read(4)), read(f.read(4)))
                polyline.add(v)
#                polyline.add(Vector(read(f.read(4)), read(f.read(4))))
#                if DEBUG: print v #, bin(v.x), bin(v.y)

#            if self.currentLayer in self.shapes:
#                self.shapes[self.currentLayer].polylines += [polyline]
#            else:
#                self.shapes[self.currentLayer] = Shape([polyline])

            if self.currentLayer in shapesByLayer:
                self.shapes[self.currentLayer].polylines += [polyline]
            else:
                self.shapes[self.currentLayer] = Shape([polyline])
        elif token == 0x11: #00:
            if DEBUG: print "ENDEL"
        elif token == 0x0002:  # SNAME
            if DEBUG: print "SNAME"
        elif token == 0x0002:  # COLROW
            if DEBUG: print "COLROW"
        elif token == 0x0002:  # NODE
            if DEBUG: print "NODE"
        elif token == 0x0002:  # TEXTTYPE
            if DEBUG: print "TEXTTYPE"
        elif token == 0x0002:  # PRESENTATION
            if DEBUG: print "PRESENTATION"
        elif token == 0x0002:  # STRING
            if DEBUG: print "STRING"
        elif token == 0x0002:  # STRANS
            if DEBUG: print "STRANS"
        elif token == 0x0002:  # MAG
            if DEBUG: print "MAG"
            magnificationFactor = read(f.read(8))
        elif token == 0x0002:  # ANGLE
            if DEBUG: print "ANGLE"
            angleDegreesCCW = read(f.read(8))
        elif token == 0x0002:  # REFLIBS
            if DEBUG: print "REFLIBS"
        elif token == 0x0002:  # FONTS
            if DEBUG: print "FONTS"
        elif token == 0x0002:  # PATHTYPE
            if DEBUG: print "PATHTYPE"
        elif token == 0x0002:  # GENERATIONS
            if DEBUG: print "GENERATIONS"
        elif token == 0x0002:  # ATTRTABLE
            if DEBUG: print "ATTRTABLE"
        elif token == 0x0002:  # EFLAGS
            if DEBUG: print "EFLAGS"
        elif token == 0x0002:  # NODETYPE
            if DEBUG: print "NODETYPE"
        elif token == 0x0002:  # PROPATTR
            if DEBUG: print "PROPATTR"
        elif token == 0x0002:  # PROPVALUE
            if DEBUG: print "PROPVALUE"
        else:
            if DEBUG: print "token not understood..."
            b2 = f.read(2)
            print ':'.join(x.encode('hex') for x in b2)

        for layer in shapesByLayer:
            self.shapes += [shapesByLayer[layer]]

    def exportGDS(self, fname, lname="GDSName", pname="pattern"):
        f = open(fname, "wb")
    
        # HEADER:
        f.write("\x00\x06\x00\x02")                 # Length 6, token 0, type 2 (2 byte)
        f.write(struct.pack(">h", self.version))    # Version 5 (default)
        
        # BGNLIB:
        f.write("\x00\x1C\x01\x02")                 # Length 28, token 1, type 5 (8 byte)
        writeTime(f)
        writeTime(f)
        
        # LIBNAME:
        f.write(struct.pack(">h", len(lname) + 4))  # Length len(str) + 4
        f.write("\x02\x06")                         # Token 2, type 6 (str)
        f.write(lname)
        
        # UNITS:
        f.write("\x00\x14\x03\x05")                 # Length 20, token 3, type 5 (8 bytes)
        write8(f, self.databaseUnitUser)        # FIX!!!
        write8(f, self.databaseUnitMeters)
        
        # BGNSTR(ucture):
        f.write("\x00\x1C\x05\x02")                 # Length 28, token 1, type 2
        writeTime(f)
        writeTime(f)
        
        # STR(ucture)NAME:
        f.write(struct.pack(">h", len(pname) + 4))  # Length len(str) + 4
        f.write("\x06\x06")                         # Token 1, type 2
        f.write(pname)
        
#        print self.shapes

        for shape in self.shapes:
            for polyline in self.polylines:

                # BOUNDARY
                f.write("\x00\x04\x08\x00")                 # Length 4, token 8, no type

                # LAYER
                f.write("\x00\x06\x0D\x02")                 # Length 6, token 8, type 2 (2 byte)
#                f.write(struct.pack(">h", key & 0x3F))      # Layer type (truncated at 63)
                f.write(struct.pack(">h", polyline.material & 0x3F))      # Layer type (truncated at 63)

                # 0x0E?
                f.write("\x00\x06\x0E\x02\x00\x00")         # Length 6, token E, type 2 (no idea what this does)

                # XY
                xy = polyline.getStippledInteger(1/self.databaseUnitUser)
                f.write(struct.pack(">h", len(xy)*4 + 4))   # Length len(str) + 4
#                print "LEN: ", struct.pack(">h", len(xy)*4 + 4), len(xy)*4 + 4
                f.write("\x10\x03")                         # Length 4, token 10, type 3
                f.write(struct.pack(">" + str(len(xy)) + "i", *xy))
    
                # ENDEL
                f.write("\x00\x04\x11\x00")                 # Length 4, token 11, no type
    
        # ENDSTR
        f.write("\x00\x04\x07\x00")             # Length 4, token 7, no type
        
        # ENDLIB
        f.write("\x00\x04\x04\x00")             # Length 4, token 4, no type

        f.close()

#    return NotImplemented

def writeTime(f):
    t = datetime.datetime.now()
    f.write(struct.pack(">hhhhhh", t.year, t.month, t.day, t.hour, t.minute, t.second))

def writeLength(f, length):
    f.write(struct.pack(">h", length))

#def read2(f):
#    bytes = f.read(8)
#    
#    integer = 0
#    
#    for byte in bytes[1:]:
#        integer <<= 8
#        integer |= byte & 0xFF
#    
#    return (-1 if bytes[0] & 0x80 else 1) * ( 16.**( (bytes[0] & 0x7F) - 78 ) ) * integer
#
#def read4(f):
#    bytes = f.read(8)
#    
#    integer = 0
#    
#    for byte in bytes[1:]:
#        integer <<= 8
#        integer |= byte & 0xFF
#    
#    return (-1 if bytes[0] & 0x80 else 1) * ( 16.**( (bytes[0] & 0x7F) - 78 ) ) * integer

def read(bytes):
#def read8(f):
#    bytes = f.read(8)

    integer = 0
    
#    print bin(ord(bytes[0]))

    for byte in bytes[1:]:
        integer <<= 8
        integer |= ord(byte) & 0xFF
#        print bin(ord(byte))

    print  (-1 if ord(bytes[0]) & 0x80 else 1) * ( 16.**( (ord(bytes[0]) & 0x7F) - 64 - len(bytes)*2 + 2 ) ) * integer
    return (-1 if ord(bytes[0]) & 0x80 else 1) * ( 16.**( (ord(bytes[0]) & 0x7F) - 64 - len(bytes)*2 + 2 ) ) * integer

            
def write8(f, num):
    if num == 0:
        f.write(f, '\x00\x00\x00\x00')
            
    negative = False
            
    if num < 0:
        num = -num
        negative = True
    
    exponent = 64
            
    while num < .0625 and exponent > 0:
        num *= 16
        exponent -= 1
    
    if exponent == 0:
        print "Error: exponent less than 0"
            
    num = int( num*(2**56) )

#    print exponent

    bytes = (0xFF00000000000000 & (((0x80 if negative else 0x00) | 0x7F & exponent) << 56)) | (0x00FFFFFFFFFFFFFF & num)

#    print bin(0xFF00000000000000 & (((0x80 if negative else 0x00) | 0x7F & exponent) << 56)), bin(0x00FFFFFFFFFFFFFF & num)

#    bytes = '\x00\x00\x00\x00'
#    bytes[0] |= (0x80 if negative else 0x00) | 0x7F & exponent
#    bytes[1] |= (0xFF0000 & num) >> 16
#    bytes[2] |= (0x00FF00 & num) >> 8
#    bytes[3] |= (0x0000FF & num)
#
#    print bytes
#    print bin(bytes)
#    print struct.pack(">q", bytes)
#    print struct.pack(">hhhh", (0xFF000000 & (((0x80 if negative else 0x00) | 0x7F & exponent))), (0x00FF0000 & num) >> 16, (0x0000FF00 & num) >> 8, (0x000000FF & num))

    f.write(struct.pack(">q", bytes))
#    f.write(struct.pack(">hhhh", (0xFF000000 & (((0x80 if negative else 0x00) | 0x7F & exponent))), (0x00FF0000 & num) >> 16, (0x0000FF00 & num) >> 8, (0x000000FF & num)))


#def read(bytes):
#    #    print hex(int(bytes.encode('hex'), 16))
##    print bin(int(bytes.encode('hex'), 16)),
##    i = 0
##    for byte in bytes:
##        print i, bin(int(byte.encode('hex'), 16))
##        i += 1
###    print "Exp:", int(bytes[0].encode('hex'), 16), "Num:", int(bytes[1:].encode('hex'), 16)
#    return readExp( int(bytes[0].encode('hex'), 16), len(bytes) )* ( int(bytes[1:].encode('hex'), 16) )
##    return readExp(struct.unpack("<L", bytes[0])[0], len(bytes)) * struct.unpack("<L", bytes[1:])[0]

def readExp(byte, length):
    print "Exp:", byte, "Sign:", (-1 if byte & 0x80 else 1), "Exponent:", (byte & 0x7F)
    return (-1 if byte & 0x80 else 1) * (16**( (byte & 0x7F) -64 +  (length-1)*8 - 4))






