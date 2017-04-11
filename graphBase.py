from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph as pg
import crystalParamBase
import pyqtgraph.exporters
import pyqtgraph.opengl as gl
# import numpy as np
# import makeBox as mkBx
# import itertools as itTl
# import makeGrids as mkGds
# import makePlanes as mkPlns
# import makeOcthedron as mkOct
# import makeCrystalStruct as mkXtlSt

class graphBase(QtGui.QWidget):
	
	def __init__(self):
		QtGui.QWidget.__init__(self)

		# Insert a layout into the main window where other widgets can be added
		self.layout = QtGui.QVBoxLayout()
		self.layout.setContentsMargins(0,0,0,0)
		self.setLayout(self.layout)

		# Insert a widget that allows for division of the layout
		self.splitterMain = QtGui.QSplitter()
		self.splitterMain.setOrientation(QtCore.Qt.Vertical)
		self.layout.addWidget(self.splitterMain)

		# View for adding crystals
		self.splitterSubAdd = QtGui.QSplitter()
		self.splitterSubAdd.setOrientation(QtCore.Qt.Vertical)
		self.splitterMain.addWidget(self.splitterSubAdd)

		# Button for adding new crystal
		self.newCrystalBut = QtGui.QPushButton('Add a New Crystal', self)
		self.newCrystalBut.clicked.connect(self.addCrystalParam)
		self.splitterSubAdd.addWidget(self.newCrystalBut)

		# add a subsplitter to allow for many crystals to be visualized
		self.splitterSubView = QtGui.QSplitter()
		self.splitterSubView.setOrientation(QtCore.Qt.Vertical)
		self.splitterMain.addWidget(self.splitterSubView)

		self.crystalParam=[]

	# Adds a news window to add a new crystal next door
	def addCrystalParam(self):
		self.crystalParam.append(crystalParamBase.crystalParamBase(self))

	# 