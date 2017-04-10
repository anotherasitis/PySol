from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import itertools as itTl
import makeBox as mkBx
import makeGrids as mkGds
import makeCrystalStruct as mkXtlSt
import makeOcthedron as mkOct
import makePlanes as mkPlns
import pyqtgraph.exporters
from pyqtgraph.dockarea import *

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000,500)

d1 = Dock("Dock1", size=(1, 1)) 
d2 = Dock('Dock2')    ## give this dock the minimum possible size
area.addDock(d1, 'left')
area.addDock(d2, 'left') 

w = gl.GLViewWidget()
w.setBackgroundColor('k')
w.setWindowTitle('Structure')
w.setCameraPosition(distance=3, azimuth=-280)
d2.addWidget(w)

subArea =  DockArea() # give this dock the minimum possible size
subD1 = Dock("Sub Dock 1", size=(1, 1))  
subD2 = Dock("Sub Dock 2", size=(1, 1))

subArea.addDock(subD1, 'top') 
subArea.addDock(subD2, )
radio1 = QtGui.QRadioButton()
radio1.setText("Radio 1")
d1.addWidget(radio1,row=0,col=0)
d1.addWidget(subArea,row=0,col=1)

if radio1.isChecked():
	print('Hellobo')

########################################### General Properties


# w.grabFrameBuffer().save('try1.bmp')

win.show()

if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()