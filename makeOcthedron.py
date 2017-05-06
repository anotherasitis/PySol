from scipy import spatial
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import itertools as itTl
import pyqtgraph.opengl as gl

def mkOctHdr(org=[0,0,0],bxSdLen=1,scl=1,transp=0.5):

	clr=[0, 1, 1, transp]
	edge=True
	smooth=True
	shader='shaded'
	glOpt='translucent'
	trOcth=np.array([list(itTl.permutations([0.25,0.5,0.75,1],4))])[0]

	norm4du=np.array([np.sqrt(2)/2, -np.sqrt(2)/2, 0, 0])
	norm4dv=np.array([np.sqrt(6)/6, np.sqrt(6)/6, -np.sqrt(2/3), 0])
	norm4dw=np.array([np.sqrt(12)/12, np.sqrt(12)/12, np.sqrt(12)/12, -np.sqrt(3)/2])
	
	ocThVert=np.array([scl*(np.sum(np.multiply(trOcth,np.tile(norm4du,
		(trOcth.shape[0],1))),axis=1)+0.5+org[0]),
		scl*(np.sum(np.multiply(trOcth,np.tile(norm4dv,
		(trOcth.shape[0],1))),axis=1)+0.5+org[1]),
		scl*(np.sum(np.multiply(trOcth,np.tile(norm4dw,
		(trOcth.shape[0],1))),axis=1)+0.5+org[2])]).T

	ocThHull=spatial.Delaunay(ocThVert)
	ocThObj=gl.MeshData(vertexes=ocThVert,faces=ocThHull.convex_hull)
	ocGrObj=gl.GLMeshItem(meshdata=ocThObj, drawEdges=edge, smooth=smooth, 
			color=(clr[0], clr[1], clr[2], clr[3]),
			shader=shader, glOptions=glOpt)

	ocGrObj.translate(-((bxSdLen/2)+org[0]), -((bxSdLen/2)+org[1]), -((bxSdLen/2)+org[2]))
	ocGrObj.rotate(55,1,0,0)
	ocGrObj.rotate(45,0,0,1)
	ocGrObj.translate(((bxSdLen/2)+org[0]), ((bxSdLen/2)+org[1]), ((bxSdLen/2)+org[2]))
	

	return ocGrObj