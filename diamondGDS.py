from shapes import precision, printPrecision, circle, arc, qBezier, thickenPolyline
from geometry import Vector, Polyline, getIntersection
from font import TTF

import matplotlib.pyplot as plt

#font = TTF("/Users/I/Desktop/diamondGDS/Arial.ttf")
font = TTF("/Users/I/Desktop/diamondGDS/Pilgiche.ttf")
#font = TTF("/Users/I/Desktop/diamondGDS/Zapfino.ttf")




string = "TrueType"
string = "1234567890"
#string = "Tr"

#names = tt.getGlyphNames()
#
##for name in names:
##    print tt['glyf'][name]
#
#ascii = None
#
#for table in tt['cmap'].tables:
#    if isinstance(table, fontTools.ttLib.tables._c_m_a_p.cmap_format_0):
#        print table
#        print table.cmap
#        print "\n"
#        ascii = table
#
#print tt
#print tt.keys()
#print tt['glyf']
#print tt['cmap']
##print tt.getGlyphNames()
##print tt.getTableData('OS/2')
#
#for char in string:
#    print ascii.cmap[ord(char)],
#
#for char in string:
#    print ascii.cmap[ord(char)]
#    print tt['glyf'][names[ord(char)]]
#    glyph = tt['glyf'][names[ord(char)]]
##    print tt['glyf'][names[ord(char)]].data
#    polyline = shapeFromGlyph(glyph)
#    print polyline
#    polyline.plot()
#
#    raw_input("Press Enter to continue...")
dv = Vector(1200,0)/1500.
v = Vector(0,3)

for char in string:
#    print ascii.cmap[ord(char)]
#    print tt['glyf'][names[ord(char)]]
#    glyph = tt['glyf'][names[ord(char)]]
#    print tt['glyf'][names[ord(char)]].data
    polyline = font[char]
#    print polyline
    (polyline + v).plot()
    v += dv



#    raw_input("Press Enter to continue...")

#    pass
#    if glyph.isComposite():
#        for compo in glyph.components:
#            for i in range(compo.numberOfContours):


#print os.curdir


#
u = Vector(2,0)
v = Vector(1,1)
print v
print v.norm()

#printPrecision()
#
#global precision
#precision = .01
#print precision
#
#printPrecision()
#
#circle(v, 1)
#
#pline = arc(v, v + Vector(1,1), v + Vector(1,-1), False)

#
#for point in pline.points:
#    print (point-v).norm()

w = Vector(2,2)

dv = Vector(0,1)
dw = Vector(1,-1)

pline = qBezier(u, v, w)
pline.add(Vector(2.25,2.25))
pline.add(Vector(2.5,2.5))
pline.add(Vector(3,2))
pline.add(Vector(3.5,1.5))
#pline.add(Vector(4,1))
#pline.add(Vector(4.5,.5))
#pline.add(Vector(5,0))
#print pline

pline2 = thickenPolyline(pline, "CUBIC", [.05,.25])
pline3 = thickenPolyline(pline + Vector(2.5,0), "CUBIC", .1)
#
#print getIntersection(v,dv,w,dw)
#
pline2.plot()
pline3.plot()
pline.plot()
#plt.fill(x, y, 'r')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()