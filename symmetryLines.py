from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import itertools as itTl
import pyqtgraph.opengl as gl

def addSymLns(org=[0,0,0],scl=1,bxSdLen=1,transp=0.8):
	items=[]
	a=bxSdLen/(2*np.sqrt(2)) #property of truncated octahedron
	color=[0.5,0.7,0.2,transp]
	glOpts='translucent'
	linewidth=3
	antialias=True

	gamma=scl*np.add(org,np.array([bxSdLen*0.5,bxSdLen*0.5,bxSdLen*0.5]))
	L=scl*np.add(org,np.array([bxSdLen*0.5+(a*np.sqrt(2)/2),bxSdLen*0.5+(a*np.sqrt(2)/2),
		bxSdLen*0.5+(a*np.sqrt(2)/2)]))
	K=scl*np.add(org,np.array([bxSdLen-(a*np.sqrt(2)/4),bxSdLen-(a*np.sqrt(2)/4),bxSdLen*0.5]))
	W=scl*np.add(org,np.array([bxSdLen*0.5+(a*np.sqrt(2)/2),bxSdLen,bxSdLen*0.5]))
	X=scl*np.add(org,np.array([bxSdLen*0.5,bxSdLen,bxSdLen*0.5]))
	U=scl*np.add(org,np.array([bxSdLen*0.5+a*np.sqrt(2)/4,bxSdLen,bxSdLen*0.5+a/np.sqrt(8)]))
	symptsAll=np.array([gamma,L,U,X,W,L,K,gamma])
	items.append(gl.GLScatterPlotItem(pos=symptsAll,color=color,glOptions=glOpts))
	items.append(gl.GLLinePlotItem(pos=(symptsAll),
		color=color,antialias=antialias, width=linewidth, glOptions=glOpts))
	
	return items
