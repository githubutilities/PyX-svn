#!/usr/bin/env python

import const, string, re, tex
from unit import unit


# PostScript-procedure definitions
# cf. file: 5002.EPSF_Spec_v3.0.pdf     

PSProlog = """
/rect {
  4 2 roll moveto 
  1 index 0 rlineto 
  0 exch rlineto 
  neg 0 rlineto 
  closepath 
} bind def
/BeginEPSF {
  /b4_Inc_state save def
  /dict_count countdictstack def
  /op_count count 1 sub def
  userdict begin
  /showpage { } def
  0 setgray 0 setlinecap
  1 setlinewidth 0 setlinejoin
  10 setmiterlimit [ ] 0 setdash newpath
  /languagelevel where
  {pop languagelevel
  1 ne
    {false setstrokeadjust false setoverprint
    } if
  } if
} bind def
/EndEPSF {
  count op_count sub {pop} repeat % Clean up stacks
  countdictstack dict_count sub {end} repeat
  b4_Inc_state restore
} bind def"""

#
# helper class for EPS files
#

bbpattern = re.compile( r"^%%BoundingBox:\s+([+-]?\d+)\s+([+-]?\d+)\s+([+-]?\d+)\s+([+-]?\d+)\s*$" )

class epsfile:

    def __init__(self, epsname, clipping = 1):
        self.epsname   = epsname
        self.clipping  = clipping
        self._ReadEPSBoundingBox()                         

    def _ReadEPSBoundingBox(self):
        'determines bounding box of EPS file epsname as 4-tuple (llx, lly, urx, ury)'
        try:
            file = open(self.epsname,"r")
        except:
            assert 0, "cannot open EPS file"	# TODO: Fehlerbehandlung

        while 1:
            line=file.readline()
            if not line:
                assert "bounding box not found in EPS file"
                raise IOError			# TODO: Fehlerbehandlung
            if line=="%%EndComments\n": 
                # TODO: BoundingBox-Deklaration kann auch an Ende von Datei verschoben worden sein
                assert "bounding box not found in EPS file"
                raise IOError			# TODO: Fehlerbehandlung
            
            bbmatch = bbpattern.match(line)
            if bbmatch is not None:
               (self.llx, self.lly, self.urx, self.ury) = map(int, bbmatch.groups())		# conversion strings->int
               break

    def __str__(self):
        try:
	    file=open(self.epsname,"r")
	except:
	    assert "cannot open EPS file"	                          # TODO: Fehlerbehandlung

	# "%f %f translate\n" % (x, y) +                             # we are already at this position

        if self.clipping:
            return """BeginEPSF
%f %f translate 
%f %f %f %f rect
clip newpath
%%BeginDocument: %s\n""" % (-self.llx, -self.lly, 
                                             self.llx, self.lly, self.urx-self.llx,self.ury-self.lly, 
                                             self.epsname) + file.read() + "%%EndDocument\nEndEPSF\n"
        else:
            return """BeginEPSF
%f %f translate 
%%BeginDocument: %s\n""" % (-self.llx, -self.lly, 
                                             self.epsname) + file.read() + "%%EndDocument\nEndEPSF\n"

#
# Exceptions
#
    
class CanvasException(Exception): pass

#
# classes
#

class canvas:

    def __init__(self, **kwargs):
        from trafo import transformation
        
        self.PSCmds = []
        self.trafo  = kwargs.get("trafo", transformation())
        self.unit   = kwargs.get("unit", unit())
        
        self._PSAddCmd("[" + `self.trafo` + " ] concat")
    
    def __str__(self):
        return reduce(lambda x,y: x + "\n%s" % str(y), self.PSCmds)

    def _PSAddCmd(self, cmd):
        self.PSCmds.append(cmd)

    def _newpath(self):
    	self._PSAddCmd("newpath")

    def _stroke(self):
    	self._PSAddCmd("stroke")

    def _fill(self):
    	self._PSAddCmd("fill")

    def _gsave(self):
        self._PSAddCmd("gsave")
	
    def _grestore(self):
        self._PSAddCmd("grestore")

    def _translate(self, x, y):
        self._PSAddCmd("%f %f translate" % self.unit.pt((x, y)))
        
    def canvas(self, **kwargs):
        subcanvas = canvas(**kwargs)
        self._gsave()
        self._PSAddCmd(subcanvas)
        self._grestore()
        return subcanvas
        
    def tex(self, **kwargs):
        texcanvas = tex.tex(**kwargs)
        self._translate(0,0)
        self._PSAddCmd(texcanvas)
        return texcanvas
	
    def draw(self, path):
        self._newpath()
        path.draw(self)
	self._stroke()
        return self
	
    def fill(self, path):
        self._newpath()
        path.fill(self)
	self._fill()
        return self

    def setlinecap(self, cap):
	self._PSAddCmd("%d setlinecap" % cap)
        return self

    def setlinejoin(self, join):
	self._PSAddCmd("%d setlinejoin" % join)
        return self
	
    def setmiterlimit(self, limit):
	self._PSAddCmd("%f setmiterlimit" % limit)
        return self

    def setdash(self, pattern, offset=0):
    	patternstring=""
    	for element in pattern:
		patternstring=patternstring + `element` + " "
    	
    	self._PSAddCmd("[%s] %d setdash" % (patternstring, offset))
        return self

    def setlinestyle(self, style, offset=0):
        self.setlinecap(style[0])
	self.setdash   (style[1], offset)
        return self

    def inserteps(self, x, y, filename, clipping=1):
        self._translate(x,y)
        self._PSAddCmd(str(epsfile(filename, clipping)))
        return self

        
    def write(self, filename, width, height, **kwargs):
        try:
  	    file = open(filename + ".eps", "w")
	except IOError:
	    assert "cannot open output file"		        # TODO: Fehlerbehandlung...

        file.write("%!PS-Adobe-3.0 EPSF 3.0\n")
        file.write("%%BoundingBox: 0 0 %d %d\n" % (1000,1000))  # TODO: richtige Boundingbox!
        file.write("%%Creator: pyx 0.0.1\n") 
        file.write("%%Title: %s.eps\n" % filename) 
        # file.write("%%CreationDate: %s" % ) 
        file.write("%%EndComments\n") 
        file.write("%%BeginProlog\n") 
        file.write(PSProlog)
        file.write("%%EndProlog\n") 
        file.write("%f setlinewidth\n" % self.unit.pt(const.linewidth.normal))
        file.write(str(self))


if __name__=="__main__":

    from tex import *
    from path import *
    from trafo import *
    from graph import *
    from const import *

    c=canvas.canvas()
    t=c.tex()
 
    #for x in range(11):
    #    amove(x,0)
    #    rline(0,20)
    #for y in range(21):
    #   amove(0,y)
    #   rline(10,0)
 
    c.draw(path( [moveto(1,1), 
                  lineto(2,2), 
                  moveto(1,2), 
                  lineto(2,1) ] 
        	)
          )
    c.draw(line(1, 1, 1,2)) 
 
    print "Breite von 'Hello world!': ",t.textwd("Hello  world!")
    print "H�he von 'Hello world!': ",t.textht("Hello world!")
    print "H�he von 'Hello world!' in large: ",t.textht("Hello world!", size = fontsize.large)
    print "H�he von 'Hello world!' in Large: ",t.textht("Hello world!", size = fontsize.Large)
    print "H�he von 'Hello world' in huge: ",t.textht("Hello world!", size = fontsize.huge)
    print "Tiefe von 'Hello world!': ",t.textdp("Hello world!")
    print "Tiefe von 'was mit q': ",t.textdp("was mit q")
    t.text(5, 1, "Hello world!")
    t.text(5, 2, "Hello world!", halign = halign.center)
    t.text(5, 3, "Hello world!", halign = halign.right)
    for angle in (-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90):
        t.text(11+angle/10, 5, str(angle), angle = angle)
        t.text(11+angle/10, 6, str(angle), angle = angle, halign = halign.center)
        t.text(11+angle/10, 7, str(angle), angle=angle, halign=halign.right)
    for pos in range(1,21):
        t.text(pos, 7.5, ".")
   
    p=path([ moveto(5,12), 
             lineto(7,12), 
             moveto(5,10), 
             lineto(5,14), 
             moveto(7,10), 
             lineto(7,14)])
   
    c.setlinestyle(linestyle.dotted)
    t.text(5, 12, "a b c d e f g h i j k l m n o p q r s t u v w x y z", hsize = 2)
    c.draw(p)
 
    p=path([ moveto(10,12), 
             lineto(12,12), 
             moveto(10,10), 
             lineto(10,14), 
             moveto(12,10), 
             lineto(12,14)])
    c.setlinestyle(linestyle.dashdotted)
    t.text(10, 12, "a b c d e f g h i j k l m n o p q r s t u v w x y z", hsize = 2, valign = valign.bottom)
    c.draw(p)
 
    p=path([moveto(5,15), arc(5,15, 1, 0, 45), closepath()])
    c.draw(p)
 
    p=path([moveto(5,17), curveto(6,18, 5,16, 7,15)])
    c.draw(p)
   
    for angle in range(20):
       s=c.canvas(trafo=translate(10,10)*rotate(angle)).draw(p)
#
#   c.setlinestyle(linestyle_solid)
#   g=GraphXY(c, t, 10, 15, 8, 6)
#   g.plot(Function("5*sin(x)"))
#   g.plot(Function("(x+5)*x*(x-5)/100"))
#   g.run()

    c.canvas(trafo=scale(0.5,0.5).rotate(20).translate(10,5)).inserteps(0,0,"ratchet_f.eps")

    c.write("example", 21, 29.7)

