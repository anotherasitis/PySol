# -*- coding: utf-8 -*-
"""
This example uses the isosurface function to convert a scalar field
(a hydrogen orbital) into a mesh for 3D display.
"""

## Add path to library (just for examples; you do not need this)

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLIsosurface')

w.setCameraPosition(distance=40)

g = gl.GLGridItem()
g.scale(2,2,1)
w.addItem(g)

import numpy as np

## Define a scalar field from which we will generate an isosurface
def psi(i, j, k, offset=(25, 25, 50)):
    Z=2
    a0=3
    n=1
    ro=2*Z/(a0*n)
    x = i-offset[0]
    y = j-offset[1]
    z = k-offset[2]
    th = np.arctan2(z, (x**2+y**2)**0.5)
    phi = np.arctan2(y, x)
    r = (x**2 + y**2 + z **2)**0.5

    #ps = (1./81.) * (2./np.pi)**0.5 * (1./a0)**(3/2) * (6 - r/a0) * (r/a0) * np.exp(-r/(3*a0)) * np.cos(th)
    ps = (1/(2*a0 * np.sqrt(6)) * np.sqrt((Z/a0)**3) * ro * r * np.exp(-ro*r/2) * np.sqrt((3/(4*np.pi)))*np.sin(th)*np.cos(phi)*np.exp(-1j * phi))**2# + \
    	#(1/(2*a0 * np.sqrt(6)) * np.sqrt((Z/a0)**3) * ro * r * np.exp(-ro*r/2) * np.sqrt((3/(4*np.pi)))*np.sin(phi)*np.sin(th)) + \
    	#(1/(2*a0 * np.sqrt(6)) * np.sqrt((Z/a0)**3) * ro * r * np.exp(-ro*r/2) * np.sqrt((3/(4*np.pi)))*np.cos(th))
    
    return ps
    
    #return ((1./81.) * (1./np.pi)**0.5 * (1./a0)**(3/2) * (r/a0)**2 * (r/a0) * np.exp(-r/(3*a0)) * np.sin(th) * np.cos(th) * np.exp(2 * 1j * phi))**2 


print("Generating scalar field..")
data = np.abs((np.fromfunction(psi, (100,100,200))))


print("Generating isosurface..")
verts, faces = pg.isosurface(data, data.max()/4.)

md = gl.MeshData(vertexes=verts, faces=faces)

colors = np.ones((md.faceCount(), 4), dtype=float)
colors[:,3] = 0.2
colors[:,2] = np.linspace(0, 1, colors.shape[0])
md.setFaceColors(colors)
m1 = gl.GLMeshItem(meshdata=md, smooth=False, shader='balloon')
m1.setGLOptions('additive')

#w.addItem(m1)
m1.translate(-25, -25, -20)

m2 = gl.GLMeshItem(meshdata=md, smooth=True, shader='balloon')
m2.setGLOptions('additive')

w.addItem(m2)
m2.translate(-25, -25, -50)