from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import itertools as itTl
import pyqtgraph.opengl as gl

def mkBx(xOr,yOr,zOr,linewidth=2,transp=1,scl=1,sz1=1):

	bxs=[]
	boxDim=np.array([np.array([0,sz1]),np.array([xOr,yOr,zOr])])
	r = [boxDim[0][0], boxDim[0][1]]
	
	for s, e in itTl.combinations(np.array(list(itTl.product(r, r, r))), 2):
		if np.sum(np.abs(s-e)) == r[1]-r[0]:
			a=np.transpose(np.array([*zip(s, e)]))
			bxSd=gl.GLLinePlotItem(pos=(a),
				color=(1,1,1,transp),antialias=True, width=linewidth, glOptions='opaque')

			bxSd.translate(boxDim[1][0],boxDim[1][1],boxDim[1][2])
			bxSd.scale(scl,scl,scl)
			bxs.append(bxSd)

	return bxs