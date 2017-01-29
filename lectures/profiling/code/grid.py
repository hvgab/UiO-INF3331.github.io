from numpy import *

class Grid2D(object):
    def __init__(self,
                 xmin=0, xmax=1, dx=0.5,
                 ymin=0, ymax=1, dy=0.5):
        
        self.xcoor = arange(xmin, xmax+dx, step=dx)
        self.ycoor = arange(ymin, ymax+dy, step=dy)

    def gridloop(self, f):
        lx = size(self.xcoor)
        ly = size(self.ycoor)
        a = zeros((lx,ly))

        for i in range(lx):
            x = self.xcoor[i]
            for j in range(ly):
                y = self.ycoor[j]
                a[i,j] = f(x, y)
        return a

g = Grid2D(dx=0.001, dy=0.001)


def myfunc(x, y):
    return sin(x*y) + y

print("Computing values...")
a = g.gridloop(myfunc)
print("done")        