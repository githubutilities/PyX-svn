#!/usr/bin/env python

# TODO: 
# - switch to affine space description (i.e. represent transformation by
#   3x3 matrix (cf. PLRM Sect. 4.3.3)? Cooler!
#

# some helper routines

def _rmatrix(angle):
    from math import pi, cos, sin
    phi = 2*pi*angle/360
	
    return  (( cos(phi), sin(phi)), 
             (-sin(phi), cos(phi)))

def _mmatrix(angle):
    from math import pi, cos, sin
    phi = 2*pi*angle/360
    
    return ( (cos(phi)*cos(phi)-sin(phi)*sin(phi), -2*sin(phi)*cos(phi)                ),
	     (-2*sin(phi)*cos(phi),                sin(phi)*sin(phi)-cos(phi)*cos(phi) ) )

def _det(matrix):
    return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

# Exception

class UndefinedResultError(ArithmeticError):
    pass

# trafo: affine transformations
	     
class trafo:
    def __init__(self, matrix=((1,0),(0,1)), vector=(0,0)):
        if _det(matrix)==0:		
	    raise UndefinedResultError, "trafo matrix must not be singular" 
	else:
            self.matrix=matrix
        self.vector=vector

    def __mul__(self, other):
        if isinstance(other, trafo):
            matrix = ( ( self.matrix[0][0]*other.matrix[0][0] + self.matrix[0][1]*other.matrix[1][0],
                         self.matrix[0][0]*other.matrix[0][1] + self.matrix[0][1]*other.matrix[1][1] ),
                       ( self.matrix[1][0]*other.matrix[0][0] + self.matrix[1][1]*other.matrix[1][0],
                         self.matrix[1][0]*other.matrix[0][1] + self.matrix[1][1]*other.matrix[1][1] )
                     )
            vector = ( self.matrix[0][0]*other.vector[0] + self.matrix[0][1]*other.vector[1] + self.vector[0],
                       self.matrix[1][0]*other.vector[0] + self.matrix[1][1]*other.vector[1] + self.vector[1] )

            # print " ( %s * %s => %s ) "% (self, other, trafo(angle=angle, vector=vector))
		      
	    return trafo(matrix=matrix, vector=vector)
	else:
	    raise NotImplementedError, "can only multiply two trafos"
    def __rmul__(self, other):				# TODO: not needed!?
        print "!"
        return other.__mul__(self)

    def matrix():
        return self.matrix

    def vector(self):
        return self.vector

    def angle(self):
        return self.angle
    
    def translate(self,x,y):
	return trafo(vector=(x,y))*self
	
    def rotate(self,angle):
	return trafo(matrix=_rmatrix(angle))*self
	
    def mirror(self,angle):
	return trafo(matrix=_mmatrix(angle))*self

    def scale(self, x, y):
        return trafo(matrix=((x, 0), (0,y)))*self

    def inverse(self):
        det = _det(self.matrix)				# shouldn't be zero, but
	try: 
          matrix = ( ( self.matrix[1][1]/det, -self.matrix[0][1]/det),
	             (-self.matrix[1][0]/det,  self.matrix[0][0]/det)
	 	   )
        except ZeroDivisionError:
	   raise UndefinedResultError, "trafo matrix must not be singular" 
        return trafo(matrix=matrix) * trafo(vector=(-self.vector[0],-self.vector[1]))
	
    def __repr__(self):
        return "matrix=%s, vector=%s" % (self.matrix, self.vector)

class translate(trafo):
    def __init__(self,x,y):
        trafo.__init__(self, vector=(x,y))
   
class rotate(trafo):
    def __init__(self,angle):
        trafo.__init__(self, matrix=_rmatrix(angle))
	
class mirror(trafo):
    def __init__(self,angle=0):
        trafo.__init__(self, matrix=_mmatrix(angle))

class scale(trafo):
    def __init__(self,x,y):
        trafo.__init__(self, matrix=((x,0),(0,y)))
        

if __name__=="__main__":
   # test for some invariants:

   def checkforidentity(trafo):
       m = max(map(abs,[trafo.matrix[0][0]-1,
                        trafo.matrix[1][0],
                        trafo.matrix[0][1],
                        trafo.matrix[1][1]-1,
	                trafo.vector[0],
	                trafo.vector[1]]))
		    
       assert m<1e-7, "tests for invariants failed" 
	    

   # trafo(angle=angle, vector=(x,y)) == translate(x,y) * rotate(angle)
   checkforidentity( translate(1,3) * rotate(15)  * trafo(matrix=_rmatrix(15),vector=(1,3)).inverse())
   
   # t*t.inverse() == 1
   t = translate(-1,-1)*rotate(72)*translate(1,1)
   checkforidentity(t*t.inverse())

   # -mirroring two times should yield identiy
   # -mirror(phi)=mirror(phi+180)
   checkforidentity( mirror(20)*mirror(20)) 
   checkforidentity( mirror(20).mirror(20)) 
   checkforidentity( mirror(20)*mirror(180+20))
   
   # equivalent notations
   checkforidentity( translate(1,2).rotate(72).translate(-3,-1)*(translate(-3,-1)*rotate(72)*translate(1,2)).inverse() )
   
   checkforidentity( rotate(40).rotate(120).rotate(90).rotate(110) )

   checkforidentity( scale(2,3).scale(1/2.0, 1/3.0) )
   
  
