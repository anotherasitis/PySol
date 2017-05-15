from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import itertools as itTl
from scipy import spatial
import pyqtgraph.opengl as gl
#Iterate through and constructure all possible locations for lattice points for a single basis
#once complete, remove duplicates and order points from smallest largest in x->y->z.
#Goes through additional basis' after completing 1

def latpts(basis = np.array([[0,0,0]]) , plv = np.array([[1,0,0],[0,1,0],[0,0,1]]) , bounds = np.array([1,1,1]) , plane = False):
	latpoints = {}
	lat_temp = {}
	f=0
	for i in basis:
		latpoints[i[0]*100+i[1]*10+i[2]]=i
		lat_temp[i[0]*100+i[1]*10+i[2]]=i
		while f<=3:
			lat_temp=latpoints
			for k in  list(latpoints):
				for j in plv:
					a= (i[0]*100+i[1]*10+i[2])+(j[0]*100+j[1]*10+j[2]) + (lat_temp[k][0]*100+lat_temp[k][1]*10+lat_temp[k][2])
					if (i[0] + j[0] + lat_temp[k][0]  <= bounds[0] and i[1] + j[1] + lat_temp[k][1] <= bounds[1] and i[2] + j[2] + lat_temp[k][2] <= bounds[2]) and (not (a in latpoints)) :
						#b = i + j
						latpoints[a] = i + j + latpoints[k]
						f=0
				f=f+1
	return latpoints