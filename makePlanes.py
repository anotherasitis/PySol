from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import itertools as itTl
from scipy import spatial

def mkPlns(plnOr,org=[0,0,0],bxSdLen=1,scl=1,res=100,transp=0.5):

	edge=True
	smooth=True
	shader='shaded'
	glOpt='translucent'
	plnClr=[1,0,1,transp]

	# plnVert=np.array([list(itTl.product([0,1],repeat=3))])[0]

	if np.array_equal(plnOr,np.array([1,1,1])):
		plnVert=np.array([[1,0,0],[0,1,0],[0,0,1]])
		# plnFc=

	elif np.array_equal(plnOr,np.array([1,1,0])):
		plnVert=np.array([[1,0,0],[1,1,0],[0,1,1],[0,0,1]])
	
	elif np.array_equal(plnOr,np.array([1,0,0])):
		plnVert=np.array([[1,0,0],[1,1,1],[1,1,0],[1,0,1]])

	plnFc=spatial.Delaunay(plnVert)
	plnDat=gl.MeshData(vertexes=plnVert,faces=plnFc.convex_hull)
	plnObj=gl.GLSurfacePlotItem(plnVert, drawEdges=edge, smooth=smooth, 
			color=(plnClr[0], plnClr[1], plnClr[2], plnClr[3]),
			shader=shader, glOptions=glOpt)

	plnObj.translate(org[0]+bxSdLen/2,org[0]+bxSdLen/2,org[0]+bxSdLen/2)
	return plnObj