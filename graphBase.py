################################################################################
# This File contains multiple classes that all require one another. Original 
# attemps to break it in to many different files for each class seem misguided. 
# In time however, this may prove to be unwise.
################################################################################

from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
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

		# self.crystalViewer=[]

		self.setUpGui()

		# self.crystalParamGroup = crystalParamBase()
		self.params = Parameter.create(name='params', type='group',
			children=[dict(name='Chemical Formula', type='str', value=''),
			dict(name='Temperature (in K)', type='float', value=293),
			dict(name='Pressure (in kPa)', type='float', value=101),
			dict(name='Add Crystal', type='action'),
			])

		self.tree.setParameters(self.params, showTop=False)
		self.params.param('Add Crystal').sigActivated.connect(self.addCrystalParam)




	def setUpGui(self):

		# Insert a layout into the main window where other widgets can be added
		self.layout = QtGui.QVBoxLayout()
		self.layout.setContentsMargins(0,0,0,0)
		self.setLayout(self.layout)

		# Insert a widget that allows for division of the layout
		self.splitterMain = QtGui.QSplitter()
		self.splitterMain.setOrientation(QtCore.Qt.Horizontal)
		self.layout.addWidget(self.splitterMain)

		# View for adding crystals
		self.splitterSubAdd = QtGui.QSplitter()
		self.splitterSubAdd.setOrientation(QtCore.Qt.Vertical)
		self.splitterMain.addWidget(self.splitterSubAdd)
		
		self.tree = ParameterTree(showHeader=False)
		self.splitterSubAdd.addWidget(self.tree)



		# # Button for adding new crystal
		# self.newCrystalBut = QtGui.QPushButton('Add a New Crystal', self)
		# self.newCrystalBut.clicked.connect(self.addCrystalParam)
		# self.splitterSubAdd.addWidget(self.newCrystalBut)

		# # add a subsplitter to allow for many crystals to be visualized
		# self.splitterSubView = QtGui.QSplitter()
		# self.splitterSubView.setOrientation(QtCore.Qt.Vertical)
		# self.splitterMain.addWidget(self.splitterSubView)

		
	# Adds a news window to add a new crystal next door
	def addCrystalParam(self):
		print('done')
		

# class crystalParamBase(pTypes.GroupParameter):

# 	def __init__(self, **kwds):
# 		self.splitterSubSubParam = QtGui.QSplitter()
# 		self.splitterSubSubParam.setOrientation(QtCore.Qt.Vertical)
# 		self.tree = ParameterTree(showHeader=False)
# 		self.newCrystalView = QtGui.QPushButton('Show Crystal Structure', self)
# 		self.newCrystalView.clicked.connect(self.addCrystalView)
# 		self.splitterSubSubParam.addWidget(self.tree)
# 		self.splitterSubSubParam.addWidget(self.newCrystalView)
# 		graphBaseWin.splitterSubAdd.addWidget(self.splitterSubSubParam)

# 		self.crystalView=[]

# 	def addCrystalView(self):
# 		self.crystalView.append(crystalViewBase.CrystalViewBase(grapBaseWin, self))

# class crystalViewBase(QtGui.QWidget):

# 	def __init__(self, graphBaseWin, crystalParams):
# 		self.area = DockArea()
# 		graphBaseWin.splitterSubView.addWidget(self.area)

# 		self.d1 = Dock("Dock1", size=(1, 1)) 
# 		self.d2 = Dock('Dock2')    ## give this dock the minimum possible size
# 		self.area.addDock(self.d1, 'left')
# 		self.area.addDock(self.d2, 'left') 

# 		self.w = gl.GLViewWidget()
# 		self.w.setBackgroundColor('k')
# 		self.w.setWindowTitle('Structure')
# 		self.w.setCameraPosition(distance=3, azimuth=-280)
# 		self.d2.addWidget(self.w)

# 		self.subArea =  DockArea() # give this dock the minimum possible size
# 		self.subD1 = Dock("Sub Dock 1", size=(1, 1))  
# 		self.subD2 = Dock("Sub Dock 2", size=(1, 1))

# 		self.subArea.addDock(self.subD1, 'top') 
# 		self.subArea.addDock(self.subD2, )
# 		self.radio1 = QtGui.QRadioButton()
# 		self.radio1.setText("Radio 1")
# 		self.d1.addWidget(self.radio1,row=0,col=0)
# 		self.d1.addWidget(self.subArea,row=0,col=1)