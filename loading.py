# Needs cleaning...

from shapes import Shape, precision, printPrecision, circle, arc, qBezier, thickenPolyline, rect
from geometry import Vector, Polyline, getIntersection, Connection
import sys, os, struct, datetime

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

    shapes = {}
    currentLayer = 0
    
    def __init__(self):
        return
#        print "Began import"
#        self.importGDS(fname)
#        print "Finished import"

    def importGDS(self, fname):
        self.shapes = {}

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

    def interpretToken(self, token_, f):
        print ':'.join(x.encode('hex') for x in token_)
        length =    int(token_[0:2].encode('hex'), 16)
        token =    int(token_[2].encode('hex'), 16)   # Rename as token
        dataType =  int(token_[3].encode('hex'), 16)
        
        DEBUG = True
        
        if DEBUG: print "LENGTH: " + str(length) + "\t" + hex(token) + "  \t",
        
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

            polyline = Polyline([], True)

            length -= 4
            
            while length > 0:
                length -= 8
                
                v = Vector(struct.unpack(">i", f.read(4))[0]*self.databaseUnitUser, struct.unpack(">i", f.read(4))[0]*self.databaseUnitUser)
#                v = Vector(int(f.read(4).encode('hex'), 16), int(f.read(4).encode('hex'), 16))
#                v = Vector(read(f.read(4)), read(f.read(4)))
                polyline.add(v)
#                polyline.add(Vector(read(f.read(4)), read(f.read(4))))
#                if DEBUG: print v #, bin(v.x), bin(v.y)

            if self.currentLayer in self.shapes:
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

        for key in self.shapes:
            for polyline in self.shapes[key].polylines:

                # BOUNDARY
                f.write("\x00\x04\x08\x00")                 # Length 4, token 8, no type

                # LAYER
                f.write("\x00\x06\x0D\x02")                 # Length 6, token 8, type 2 (2 byte)
                f.write(struct.pack(">h", key & 0x3F))      # Layer type (truncated at 63)

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
    
        # ENDEL
        f.write("\x00\x04\x07\x00")             # Length 4, token 7, no type
        
        # ENDEL
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






