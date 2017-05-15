from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

def fermiSurf(latPts=(0,0,0)):
	m=90
	scl = 0.011256637
	## Define a scalar field from which we will generate an isosurface
	def psi(i, j, k, offset=(0, 0, 0)):

		x = (i-offset[0])*2*np.pi/50
		y = (j-offset[1])*2*np.pi/50
		z = (k-offset[2])*2*np.pi/50
		a = 5.14e-10
		e = 1.60218e-19
		Ry = 13.6
		me = 9.10938E-31 #kg
		hbar = 1.05459E-34#
		fineStruct = 0.0072973525664
		ro = ((me*e*e)/(hbar*hbar)*np.linalg.norm(np.array([0.25,0.25,0.25])))
		bondE_coupling = np.array(2*(1+ro)*np.exp(-ro))
		alpha = 1.6

		ps= -alpha - 4*bondE_coupling*( np.cos(0.5*x)*np.cos(0.5*y) \
			+ np.cos(0.5*z)*np.cos(0.5*y) \
			+ np.cos(0.5*z)*np.cos(0.5*x) )
	    
		return ps
	   
	data = np.fromfunction(psi, (m,m,m))
	verts, faces = pg.isosurface(data, data.max()/4)
	md = gl.MeshData(vertexes=verts, faces=faces)
	colors = np.ones((md.faceCount(), 4), dtype=float)
	colors[:,3] = 0.6
	colors[:,2] = 0#np.linspace(0, 1, colors.shape[0])
	colors[:,1] = 0.270588
	colors[:,0] = 0.7
	md.setFaceColors(colors)
	m1 = gl.GLMeshItem(meshdata=md, smooth=False, shader='balloon')
	m1.setGLOptions('additive')
	m1.scale(scl,scl,scl)

	return m1