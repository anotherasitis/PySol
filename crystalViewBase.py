from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph as pg
import crystalParamBase
import pyqtgraph.exporters
import pyqtgraph.opengl as gl

class crystalViewBase(QtGui.QWidget):

	def __init__(self, graphBaseWin, crystalParams):
		self.area = DockArea()
		graphBaseWin.splitterSubView.addWidget(self.area)

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