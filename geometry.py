import math
import matplotlib.pyplot as plt

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def even(x):
    return math.ceil(x/2.) == math.floor(x/2.)

####  MATERIALS  ################################################################################
class Materials: ################################################################################
    materialsList = []
    materialsDict = {}
    size = 0

    def __init__(self, mList):
#        print materials
        self.add(mList)
    
    def __repr__(self):
        string = "The current materials are:\n"
        for material in self.materialsList:
            string += str(material) + "\n"
        return string
    
    def add(self, mList):
        if isinstance(mList, list):
            if isinstance(mList[0], str):
                self.addSingle(mList)
            else:
                for material in mList:
#                    print material
                    self.addSingle(material)

    def addSingle(self, material):
#        print material
        newMaterial = Material(material[0], material[1], material[2], self.size)
#        self.materialsList += [newMaterial]
        self.materialsList.extend([newMaterial])
        self.materialsDict[newMaterial.name] = newMaterial.i
        self.size += 1

    def __getitem__(self, i):
        if isinstance(i, int) and i < self.size:
            return self.materialsList[i]
        elif isinstance(i, str) and i in materialsDict:
            return self.materialsList[self.materialsDict[i]]
        else:
            return None

class Material:
    name = "Text"
    color = "#000000"
    border = "#CCCCCC"
    i = 0

    def __init__(self, name, color, border, i=0):
        self.name = name
        if False:
            self.color = color
            self.border = border
        else:
            self.color = border
            self.border = color
        self.i = i
    
    def __repr__(self):
        return "  Material " + self.name + " with color " + self.color + " and outline " + self.border

    def __eq__(self, other):
        return self.i == other.i

materials = Materials([["Text", "#000000", "#CCCCCC"],
                       ["GaP",  "#CC6666", "#e6b3b3"],
                       ["NbN",  "#336600", "#99ff33"],
                       ["Au",   "#FFCC00", "#ffe680"]])

print materials


####  MATRIX  ##################################################################################
class Matrix: ##################################################################################
    a = 1; c = 0    # Generic 2x2 matrix
    b = 0; d = 1
    
    e = 0           # Vector offset
    f = 0
    
    ##### INITIATION #####======================================================================
    def __init__(self, a=None, b=None, c=None, d=None, e=None, f=None):
        if a is not None and b is not None and c is not None and d is not None and e is not None and f is not None: # If everything is there, initialize normally,
            self.a = a; self.c = c
            self.b = b; self.d = d
        
            self.e = e
            self.f = f
        elif a is not None and b is not None and c is not None and d is not None:   # If only e and f are missing, initialize everything except for e and f
            self.a = a; self.c = c
            self.b = b; self.d = d
        elif a is not None:                                     # If everything is there, initialize normally,
            if isinstance(a, list) or isinstance(a, tuple):     # If a list/tuple was given, fill the matrix with the list
                if len(a) >= 4:
                    self.a = a[0]; self.c = a[1]
                    self.b = a[2]; self.d = a[3]
                else:
                    print "List not long enough; matrix set to identity."
                
                if len(a) >= 6:
                    self.e = a[4]
                    self.f = a[5]
            elif isinstance(a, int) or isinstance(a, float):    # If a number was given, return the rotation matrix for 'a' radians.
                s = math.sin(a)
                c = math.cos(a)
                                
                self.a = c; self.c = -s
                self.b = s; self.d = c
            else:                                               # Otherwise, return the identity matrix...
                print "Type not understood; matrix set to identity."
        
    
    ##### OPERATORS #####=======================================================================
    def __repr__(self): # Returns the Matrix in [ a, c; b, d ] with offset [ e, f ] form
        return "matrix [ " + str(self.a) + ", " + str(self.c) + " ; " + str(self.b) + ", " + str(self.d) + " ] with offset [ " + str(self.e) + ", " + str(self.f) + " ]"
    
    # Inequalities, based on determinant, except for == and !=
    def __lt__(self, other):
        if not isinstance(other, Matrix): return False
        return self.det() <  other.det()
    def __le__(self, other):
        if not isinstance(other, Matrix): return False
        return self.det() <= other.det()
    def __eq__(self, other):
        if not isinstance(other, Matrix): return False
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d and self.e == other.e and self.f == other.f
    def __ne__(self, other):
        if not isinstance(other, Matrix): return False
        return not (self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d and self.e == other.e and self.f == other.f)
    def __gt__(self, other):
        if not isinstance(other, Matrix): return False
        return self.det() >  other.det()
    def __ge__(self, other):
        if not isinstance(other, Matrix): return False
        return self.det() >= other.det()
    
    # Sums etc
    def __add__(self, other):   # To this matrix, add another matrix or vector
        if isinstance(a, Matrix):   return Matrix(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d, self.e + other.e, self.f + other.f)
        elif isinstance(a, Vector): return Matrix(self.a, self.b, self.c, self.d, self.e + other.x, self.f + other.y)
        else:                       return NotImplemented
    def __sub__(self, other):   # From this matrix, subtract another matrix or vector
        if isinstance(a, Matrix):   return Matrix(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d, self.e - other.e, self.f - other.f)
        elif isinstance(a, Vector): return Matrix(self.a, self.b, self.c, self.d, self.e - other.x, self.f - other.y)
        else:                       return NotImplemented
    def __mul__(self, other):   # Multiplication by many types
        if isinstance(other, Matrix):       # Matrix-Matrix multiplication
            return Matrix(self.a*other.a + self.c*other.b,
                          self.a*other.c + self.c*other.d,
                          self.b*other.a + self.d*other.b,
                          self.b*other.c + self.d*other.d,
                          self.e + other.e,
                          self.f + other.f)
        elif isinstance(other, Vector):     # Matrix-Vector multiplication
            return Vector(self.a*other.x + self.c*other.y + self.e, self.b*other.x + self.d*other.y + self.f)
        elif isinstance(other, Connection): # Matrix-Connection multiplication
            return Connection(Vector(self.a*other.v.x + self.c*other.v.y + self.e,
                                     self.b*other.v.x + self.d*other.v.y + self.f),
                              Vector(self.a*other.dir.x + self.c*other.dir.y,
                                     self.b*other.dir.x + self.d*other.dir.y),
                              other.wid)
        elif isinstance(other, int) or isinstance(other, float):    # Matrix-Scalar multiplication
            return Matrix(self.a*other, self.b*other, self.c*other, self.d*other)
        else:
            print NotImplemented
    def __div__(self, scalar):
        if scalar == 0:
            print "Error, tried to divide by zero!"
            return Vector(0,0)
        else:
            return Vector(self.x/scalar, self.y/scalar)
    def __neg__(self):
        return Matrix(-self.a, -self.b, -self.c, -self.d, -self.e, -self.f)
    def __pos__(self):
        return self
    def __abs__(self):
        return self.det()
    
    def setOffset(self, v):
        if isinstance(other, Vector):
            self.e = v.x
            self.f = v.y
        else:
            return NotImplemented
    def getOffset(self):
        return Vector(self.e, self.f)
    
    def det(self):      # Returns the determinant of the matrix
        return self.x*self.x + self.y*self.y
    
    def __len__(self):  # len( mat ) = mat.det()
        return self.det()

####  VECTOR  ##################################################################################
class Vector: ##################################################################################
    x = 0
    y = 0

    ##### INITIATION #####======================================================================
    def __init__(self, x=0, y=0): # Initialize vector as (x,y)
        self.x = x
        self.y = y
        
    ##### OPERATORS #####=======================================================================
    def __repr__(self):     # Returns the vector in [ x, y ] form
        return "[ " + str(self.x) + ", " + str(self.y) + " ]"

    # Inequalities
    def __lt__(self, other):
        if not isinstance(other, Vector): return False
        return self.norm() <  other.norm()
    def __le__(self, other):
        if not isinstance(other, Vector): return False
        return self.norm() <= other.norm()
    def __eq__(self, other):
        if not isinstance(other, Vector): return False
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        if not isinstance(other, Vector): return False
        return not (self.x == other.x and self.y == other.y)
    def __gt__(self, other):
        if not isinstance(other, Vector): return False
        return self.norm() >  other.norm()
    def __ge__(self, other):
        if not isinstance(other, Vector): return False
        return self.norm() >= other.norm()

    # Sums etc
    def __add__(self, other):
        if isinstance(other, Vector):   return Vector(self.x + other.x, self.y + other.y)
        else:                           return NotImplemented
    def __sub__(self, other):
        if isinstance(other, Vector):   return Vector(self.x - other.x, self.y - other.y)
        else:                           return NotImplemented
    def __mul__(self, other):
        if isinstance(other, Vector):   return self.x*other.x + self.y*other.y
        if isinstance(other, Matrix):   return Vector(self.x*other.a + self.y*other.b, self.x*other.c + self.y*other.d)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x*other, self.y*other)
        else:
            return NotImplemented
    def __div__(self, scalar):
        if scalar == 0:
            print "Error, tried to divide by zero!"
            return Vector(0,0)
        else:
            return Vector(self.x/scalar, self.y/scalar)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def __pos__(self):
        return self
    def __abs__(self):
        return self.norm()
    
    def copy(self):
        return Vector(self.x, self.y)
        
    ##### SIMPLE VECTOR #####===================================================================
    def dot(self, other):                       # Returns the dot product of self and other
        if isinstance(other, Vector):
            return self * other
        else:
            return NotImplemented

    def perpDot(self, other):                   # Returns the dot product of self.perp() and other
        if isinstance(other, Vector):
            return self.x*other.y - self.y*other.x
        else:
            return NotImplemented

    def cross(self, other):                     # Because we're in 2D, this returns +1 if the resulting vector is up, -1 if the resulting vector is down, and 0 if the vecotrs are parallel or antiparallel.
        return sign(self.x*other.y - other.x*self.y)

    def mean(self, other):
        return Vector((self.x + other.x)/2, (self.y + other.y)/2)

    def norm2(self):                            # Returns the square of the norm of the vector
        return self.x*self.x + self.y*self.y
    def norm(self):                             # Returns the norm of the vector
        #return sqrt(self.norm())               # Not sure which one is faster...
        return math.hypot(self.x, self.y)

    def __len__(self):                          # len( v ) = v.norm()
        return self.norm()

    def unit(self):                             # Returns the vector, normalized
        n = self.norm()
        return Vector(self.x/n, self.y/n)
    def Unit(self):                             # Normalize the vector and return it
        n = self.norm()
        
        self.x /= n
        self.y /= n
        
        return self
    
    def rotate(self, radians):                  # Returns the vector, rotated CCW by 'radians' radians.
        s = math.sin(radians)
        c = math.cos(radians)
        
        return Vector(self.x*c - self.y*s, self.x*s + self.y*c)
    def Rotate(self, radians):                  # Rotates the vector by 'radians' radians CCW, then returns it.
        s = math.sin(radians)
        c = math.cos(radians)
        
        self.x = self.x*c - self.y*s
        self.y = self.x*s + self.y*c
        
        return self
    
    def perp(self):                             # Returns the vector, rotated CCW by 90deg
        return Vector(-self.y, self.x)
    def Perp(self):                             # Rotates the vector 90deg CCW, then returns it.
        self.x = -self.y
        self.y = self.x
        
        return self
    
    def plot(self):                             # Plots the polyline using MATPLOTLIB
        plt.plot(self.x, self.y, 'or')

####  POLYLINE  ################################################################################
class Polyline: ################################################################################
    points = []
    closed = False
    size = 0
    material = 1
    reverse = False
#    bbll = Vector(0,0)  # The lower-left
#    bbur = Vector(0,0)  # and upper-right corners of the bounding box (decrepetated).

    ##### INITIATION #####======================================================================
    def __init__(self, points=[], closed=False, reverse=False, material=1):    # Initialize open/closed polyline with points
        self.points = points
        self.closed = closed
        self.size = len(points)
        self.reverse = reverse      # 'reversed' decides whether the start of the polyline is the first index in the list or the last...
        self.material = material
        
    ##### OPERATORS #####=======================================================================
    def __repr__(self):     # Returns the vector in (x,y) form
        if self.size > 0:
            string = "  This polyline contains the points:"
            for point in self.points:
                string += "\n    " + str(point)
            return string + "\n"
        else:
            return "  This polyline is empty..."

    # Inequalities
    def __lt__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size <  other.size
    def __le__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size <= other.size
    def __eq__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size == other.size
    def __ne__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size != other.size
    def __gt__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size >  other.size
    def __ge__(self, other):
        if not isinstance(other, Polyline): return False
        return self.size >= other.size

    # Sums etc
    def __add__(self, other):           # If vector is added, adds vector from each point in polyline
        if isinstance(other, Vector):
            return Polyline( list( point + other for point in self.points ), self.closed)
        elif isinstance(other, Polyline):
            return NotImplemented
        else:
            return NotImplemented
    def __sub__(self, other):           # If vector is subtracted, subtracts vector from each point in polyline
        if isinstance(other, Vector):
            return Polyline( list( point - other for point in self.points ), self.closed)
        elif isinstance(other, Polyline):
            return NotImplemented
        else:
            return NotImplemented
    def __mul__(self, other):           # Multiplies every point by other. Type checking left to the Vector class.
        return Polyline( list( other*point for point in self.points ), self.closed)
    def __div__(self, scalar):
        return Polyline( list( point/other for point in self.points ), self.closed)
    def __neg__(self):
        return Polyline( list(self.points), self.closed, not self.reverse)
    def __pos__(self):
        return Polyline( list(self.points), self.closed, self.reverse)
    def __abs__(self):
        return NotImplemented
    
    def __getitem__(self, i):           # Gets the point at index 'i', taking 'reverse' into account.
        if i >= self.size or i < 0:
            print "Error: Index out of range..."
            return None
        else:
            if self.reverse:
                return self.points[self.size - 1 - i]
            else:
                return self.points[i]
        
    ##### FUNCTIONS #####===================================================================
    def add(self, other):   # Adds a vector (or another polyline) to this polyline. If points are the same as the previous, do not add. Returns whether a point was added.
        if isinstance(other, Vector):
            if self.size > 0 and self.points[self.size-1] != other:
                self.points.extend([other])
                self.size += 1
                return True
            if self.size == 0:
                self.points.extend([other])
                self.size += 1
                return True
            else:
                return False
        elif isinstance(other, Polyline):
            if other.size > 0 and self.size > 0:
                start = 0
                while start < other.size and self.points[self.size - 1] == other.points[start]:
                    start += 1
                self.points += other.points[start:]
                self.size += len(other.points[start:])
            elif self.size == 0:
                self.points = other.points[:]
                self.size = other.size
        else:
            print NotImplemented

    def copy(self):     # Returns a copy of this polyline (because you actually have to worry about this in worst-language-Python)
        return Polyline(list(self.points), self.closed, self.size)
    
    def length(self):   # Returns the length of the polyline in 2D space. Important: this is different from size...
        if self.size <= 1:
            return 0
        else:
            toReturn = 0
            for x in range(1, self.size):
                toReturn += (self.points[x] - self.points[x-1]).norm()
            return toReturn

    def sizeCalc(self): # Returns the number of points in this polyline
        self.size = len(self.points)
        return self.size
    def __len__(self):
        return self.size
    
    def getStippledInteger(self, scalar):
        toReturn = [None]*(self.size*2)
        
        toReturn[::2] =  list(point.x*scalar for point in self.points)
        toReturn[1::2] = list(point.y*scalar for point in self.points)
        
        toReturn.extend([self.points[0].x*scalar])
        toReturn.extend([self.points[0].y*scalar])
    
        return toReturn # Error Correct!

    def plot(self):     # Plots the polyline using MATPLOTLIB
        if self.size > 0:
            xlist = list(point.x for point in self.points)
            ylist = list(point.y for point in self.points)
            
            if self.closed:
                plt.fill(xlist, ylist, color=materials[self.material].border, facecolor=materials[self.material].color)
            else:
                plt.plot(xlist, ylist)

    def plotPerp(self): # Plots the perps of the polyline using MATPLOTLIB
        if self.size > 0:
            for i in range(0, self.size - 1):
                plotLine( self.points[i], self.points[i] + (self.points[i+1] - self.points[i]).perp().unit() )

    def perp(self, i, type, width=1.0, vector=None):    # 'vector' used for i=0, i=size-1
#        print type, width
        if self.size < 2:
            print "Error; not enough points"
            return None
		
        if i < 0 or i >= self.size:
            print "Error; out of range"
        elif i == 0:
#            print "Case1"
            if vector == None:
                v = (self.points[1] - self.points[0]).unit()
                w = v
            else:
                v = vector.unit()
                w = (self.points[1] - self.points[0]).unit()
        elif i == self.size-1:
#            print "Case2"
            if vector == None:
                v = (self.points[self.size-1] - self.points[self.size-2]).unit()
                w = v
            else:
                v = vector.unit()
                w = (self.points[self.size-1] - self.points[self.size-2]).unit()
        else:
#            print "Case3"
#            print self.points[i-1], self.points[i], self.points[i+1]
            v = (self.points[i] - self.points[i-1]).unit()
            w = (self.points[i+1] - self.points[i]).unit()
        
#        print v, w, math.sqrt((1 + v * w)/2)

        if type == 0:   # Sharp
#            print v, w
#            print i, 1 + v * w
            return self.points[i] + (v.perp() + w.perp()).unit() * width / math.sqrt((1 + v * w)/2) #math.cos(math.acos(v * w)/2)
        if type == 1:   # Round
            return NotImplemented
        if type == 2:   # Blunt
            return NotImplemented
        if type == 3:   # Bezier
            return NotImplemented
    
    def getIntersections(self, other):
        intersections = []
        
        for i in range(0 if self.closed  else 1, self.size):
            for j in range(0 if other.closed else 1, other.size):
                if i == 0:  v = self[self.size - 1]
                else:       v = self[i - 1]
                
                if j == 0:  w = other[other.size - 1]
                else:       w = other[j - 1]
                
                intersection = getLineIntersection(v, self[i], w, other[j])
#                print intersection, i, j, v, self[i], w, other[j]

                if isinstance(intersection, Vector):
#                    intersections += [ [intersection, i, j] ]
                    intersections.extend([ [intersection, i, j] ])
                    intersection.plot()
#                    print intersection, i, j
#                    print self[i], v, other[j], w
                    plotLine(self[i], v)
                    plotLine(other[j], w)
        return intersections
    def getSelfIntersections(self):
        return NotImplemented
    
    def isInside(self, v):
        if self.closed:
            return NotImplemented
        print "Error: An unclosed line does not have an inside or outside..."
        return None
    
    def union(self, other):
        if self.closed:
            toReturn = Polyline([], True, self.reverse)
            
            intersections = self.getIntersections(other)

#            print intersections

            if not even(len(intersections)):
                print "Not an even number of intersections! Not sure how this happened..."
                return None
            
            addModeSelf = True
            i = 0
            j = 0
            
#            print self.reverse, other.reverse

            for intersection in intersections:
#                print "Intersection"
#                print i,j, len(toReturn)
                if addModeSelf:
                    if self.reverse:
                        toReturn.points += reversed(self.points[(self.size - intersection[1]):(self.size - i)]) # Change this (and below) to .extend() for speed...
                        toReturn.points += [intersection[0]]
                    else:
#                        print i
#                        print self.points[0]
                        toReturn.points += self.points[i:intersection[1]]
                        toReturn.points += [intersection[0]]
                else:
                    if other.reverse:
                        if j <= intersection[2]:
                            toReturn.points += reversed(other.points[(other.size - intersection[2]):(other.size - j)])
                        if j > intersection[2]:
                            toReturn.points += reversed(other.points[0:(other.size - j)])
                            toReturn.points += reversed(other.points[other.size - intersection[2]:other.size])
                        toReturn.points += [intersection[0]]
                    else:
                        if j <= intersection[2]:
                            toReturn.points += other.points[j:intersection[2]]
                        if j > intersection[2]:
                            toReturn.points += other.points[j:other.size]
                            toReturn.points += other.points[0:intersection[2]]
                        toReturn.points += [intersection[0]]
                            
                addModeSelf = not addModeSelf
                i = intersection[1]
                j = intersection[2]
#                print i,j, len(toReturn)

            if self.reverse:
                toReturn.points += reversed(self.points[0:(self.size - i)])
            else:
                toReturn.points += self.points[i:self.size]
#                print self.points[i:self.size-1]
#                print self.points[self.size-1]

            toReturn.size = len(toReturn.points)
            
            print "AREA:  ", toReturn.area()
            
            if toReturn.area() <= 0:    # This might induce infinte recursion...
                return Polyline.union(other,self)
#            print toReturn.points
#            
#            print toReturn

            return toReturn
        else:
            return NotImplemented
    def Union(self, other):
        return NotImplemented

    def getBoundingBox(self):
        if self.size >= 1:
            bbll = self.points[0].copy()
            bbur = self.points[0].copy()
        
            for point in self.points:
                if  bbur.x < point.x:
                    bbur.x = point.x
                elif bbll.x > point.x:
                    bbll.x = point.x
                if  bbur.y < point.y:
                    bbur.y = point.y
                elif bbll.y > point.y:
                    bbll.y = point.y
            return [bbll, bbur]
        else:
            return None

    def area(self):
        if self.closed:
            sum = self.points[self.size-1].perpDot(self.points[0])
            for i in range(0, self.size-1):
                sum += self.points[i].perpDot(self.points[i+1])
            return (1 if self.reverse else -1)*sum/2
        else:
            return 0

####  CONNECTION  ##############################################################################
class Connection: ##############################################################################
    v =   Vector(0,0)
    dir = Vector(1,0)
    wid = 1.0
    material = 1
    
    ##### INITIATION #####======================================================================
    # Initialize connection at 'point' pointing int the 'direction' direction with width 'width'
    def __init__(self, point, direction, width, material=1):
        self.v = point
        self.dir = direction.unit()
        self.wid = width
        self.material = material
    
    ##### OPERATORS #####=======================================================================
    # Returns a string
    def __repr__(self):
        return "Connection at " + str(self.v) + " pointing toward " + str(self.dir) + " with width " + str(self.wid)
    
    # Inequalities
    def __lt__(self, other):
        return self.width <  other.width
    def __le__(self, other):
        return self.width <= other.width
    def __eq__(self, other):
        return self.width == other.width
    def __ne__(self, other):
        return self.width != other.width
    def __gt__(self, other):
        return self.width >  other.width
    def __ge__(self, other):
        return self.width >= other.width
    
    # Sums etc
    def __add__(self, other):
        if isinstance(other, Vector):
            return Connection(self.v + other, self.dir.copy(), self.wid)
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Connection(self.v - other, self.dir.copy(), self.wid)
    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Connection(other * self.v, (other * self.dir) - other.getOffset(), self.wid)
    def __div__(self, scalar):
        if scalar == 0:
            print "Error, tried to divide by zero!"
            return Vector(0,0)
        else:
            return Shape( list( polyline/other for polyline in self.polylines ), list(self.connections))
    def __neg__(self):
        return Connection(self.v, -self.dir, self.wid)
    def __pos__(self):
        return self
    def __abs__(self):
        return self.width

    def matrix(self):
        return Matrix(-self.dir.x, -self.dir.y, self.dir.y, -self.dir.x, self.v.x, self.v.y)

    def plot(self):
        plotLine(self.v, self.v+self.dir)


def getIntersection(a, da, b, db):
    da.Unit()
    db.Unit()
    
    if da.y*db.x - da.x*db.y != 0:
        x = ( (a.x - b.x)*db.y - (a.y - b.y)*db.x ) / (da.y*db.x - da.x*db.y)
        #        if db.x != 0:
        #            y = (a.x - b.x - x*da.x) / db.x
        #        else:
        #            y = (a.y - b.y - x*da.y) / db.y
        
        return a + da*x
    else:
        print "Vectors are parallel or something is wrong..."

def getPerpIntersection(a, da, b): # Finds a 'c' such that (c-a) is perpendicular to (c-b) and (c-a) is in the direction of da.
    return NotImplemented

def getLineIntersection(a, b, A, B, tellTruth=False):    # Gets the intersection between the lines defined by a -> b and A -> B. If no intersection, returns False. 'tellTruth' is for the special case where the lines are identical.
    # Easy checks:
    if (a.x < A.x and a.x < B.x and b.x < A.x and b.x < B.x) or (a.x > A.x and a.x > B.x and b.x > A.x and b.x > B.x): # No x overlap
        return False
    if (a.y < A.y and a.y < B.y and b.y < A.y and b.y < B.y) or (a.y > A.y and a.y > B.y and b.y > A.y and b.y > B.y): # No y overlap
        return False

    # Also easy checks:
    if a == A and b == B:                       # Same
        return [a, b] if tellTruth else False
    elif a == B and b == A:                     # Anti-same
        return [a, b] if tellTruth else False
    elif a == A:                                # a
        return a if tellTruth else False
    elif a == B:                                # a
        return a
    elif b == A:                                # b
        return b
    elif b == B:                                # b
        return b if tellTruth else False

    # Check if parallel:
    if (b - a).perp()*(B - A) == 0:
        if (b - a).perp()*(B - a) == 0:         # Are they on the same line?
            return NotImplemented
        else:                                   # Otherwise, there is no intersection...
            return False

    dx = b.x - a.x
    dy = b.y - a.y
    
    dX = B.x - A.x
    dY = B.y - A.y

    if dx != 0 and dX == 0:                     # a -> b vertical
        if (A.x >= a.x and A.x <= b.x) or (A.x <= a.x and A.x >= b.x):
            return Vector(A.x, a.y - (dy/dx)*(A.x-a.x))
        else:
            return False
    elif dx == 0 and dX != 0:                   # A -> B vertical
        if (a.x >= A.x and a.x <= B.x) or (a.x <= A.x and a.x >= B.x):
            return Vector(a.x, A.y - (dY/dX)*(a.x-A.x))
        else:
            return False
    else:                                       # Both not vertical
        x = ( (a.y - A.y) - ((dy/dx)*a.x - (dY/dX)*A.x) ) / ((dY/dX) - (dy/dx))
        if ((x >= a.x and x <= b.x) or (x <= a.x and x >= b.x)) and ((x >= A.x and x <= B.x) or (x <= A.x and x >= B.x)):
            return Vector(x, a.y + (dy/dx)*(x-a.x))
        else:
            return False

def plotLine(a, b):
    xlist = [a.x, b.x]
    ylist = [a.y, b.y]
    plt.plot(xlist, ylist, 'r')









