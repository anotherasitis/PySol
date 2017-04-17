from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import itertools as itTl
from scipy import spatial

#Iterate through and constructure all possible locations for lattice points for a single basis
#once complete, remove duplicates and order points from smallest largest in x->y->z.
#Goes through additional basis' after completing 1
#Final array latpoints will have the defined ordering structure per basis, followed by the points of the n+1 basis.

def latpts(basis = [0,0,0] , plv = [[1,0,0],[0,1,0],[0,0,1]] , bounds = [1,1,1] , plane = false):

latpoints = {}

for i in basis[...,]:
	latpoints[i[0]*100+i[1]*10+i[2]]=i
	for j in plv[...,]:
		#Note bounds should be adjusted to be the solutions to being in or outside a volume (spacial testing for non rectangular shapes)
		if i[0] + j[0] <= bounds[0] and i[1] + j[1] <= bounds[1] and i[2] + j[2] <= bounds[2]:
			a=(i[0]*100+i[1]*10+i[2])+(j[0]*100+j[1]*10+j[2])
			latpoints[a] = i + j

#print (latpoints)

return latpoints