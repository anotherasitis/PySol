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
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import types as pTypes

class graphBase(QtGui.QWidget):
	
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.layout = QtGui.QVBoxLayout()
		self.layout.setContentsMargins(0,0,0,0)
		self.setLayout(self.layout)

		self.splitter = QtGui.QSplitter()
		self.splitter.setOrientation(QtCore.Qt.Vertical)

		self.layout.addWidget(self.splitter)
		
		self.tree = ParameterTree(showHeader=False)
		self.splitter.addWidget(self.tree)

		self.area = DockArea()
		self.splitter.addWidget(self.area)

		self.d1 = Dock("Dock1", size=(1, 1)) 
		self.d2 = Dock('Dock2')    ## give this dock the minimum possible size
		self.area.addDock(self.d1, 'left')
		self.area.addDock(self.d2, 'left') 

		self.w = gl.GLViewWidget()
		self.w.setBackgroundColor('k')
		self.w.setWindowTitle('Structure')
		self.w.setCameraPosition(distance=3, azimuth=-280)
		self.d2.addWidget(self.w)

		self.subArea =  DockArea() # give this dock the minimum possible size
		self.subD1 = Dock("Sub Dock 1", size=(1, 1))  
		self.subD2 = Dock("Sub Dock 2", size=(1, 1))

		self.subArea.addDock(self.subD1, 'top') 
		self.subArea.addDock(self.subD2, )
		self.radio1 = QtGui.QRadioButton()
		self.radio1.setText("Radio 1")
		self.d1.addWidget(self.radio1,row=0,col=0)
		self.d1.addWidget(self.subArea,row=0,col=1)

		if self.radio1.isChecked():
			print('Hellobo')