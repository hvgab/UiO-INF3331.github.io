from numpy import *

class Grid2D(object):
    def __init__(self,
                 xmin=0, xmax=1, dx=0.5,
                 ymin=0, ymax=1, dy=0.5):
	""" Initialises a new 2D grid object """
        
        self.xcoor = arange(xmin, xmax+dx, step=dx)
        self.ycoor = arange(ymin, ymax+dy, step=dy)

    def gridloop(self, f):
	""" Evaluate a function to each vertex of the grid.
	    Returns: An array of all function values
	"""
        lx = size(self.xcoor)
        ly = size(self.ycoor)
        a = zeros((lx,ly))

        for i in range(lx):
            x = self.xcoor[i]
            for j in range(ly):
                y = self.ycoor[j]
                a[i,j] = f(x, y)
        return a

def myfunc(x, y):
    return sin(x*y) + y

# Initialise grid
g = Grid2D(dx=0.001, dy=0.001)

print("Computing values...")
a = g.gridloop(myfunc)
print("done")        