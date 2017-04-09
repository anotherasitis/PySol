from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import itertools as itTl

def mkGds(dims,bxSdLen=1,scl=1):
	
	lowCor=dims.min()
	topCor=bxSdLen+dims.max()
	grTD=np.sign(lowCor)

	if grTD==0:
		grTD=1

	if lowCor>0:
		lowCor=0

	if topCor<0:
		topCor=0

	dim=topCor-lowCor
	gtDim=grTD*(dim)/2
	lcDim=grTD*abs(lowCor)*(dim)
	grdSep=dim/20

	g = gl.GLGridItem(glOptions='opaque')
	g.translate(gtDim, gtDim, lcDim)
	g.setSize(x=dim,y=dim,z=dim)
	g.setSpacing(x=grdSep,y=grdSep,z=grdSep)
	g.scale(scl,scl,scl)
	
	return g