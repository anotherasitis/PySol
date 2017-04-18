################################################################################
# This File contains multiple classes that all require one another. Original 
# attemps to break it in to many different files for each class seem misguided. 
# In time however, maybe this will prove unwise.
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

class graphBase(QtGui.QWidget):
	
	def __init__(self):
		QtGui.QWidget.__init__(self)

		self.dockAreaList = {}

		self.setUpGui()
		self.params = crystalParamBase.crytalParamInitialize()

		self.tree.setParameters(self.params, showTop = False)
		self.params.param('Add Crystal').sigActivated.connect(self.addCrystalParam)
		self.params.param('Crystals').sigChildRemoved.connect(self.crystalWindowRemove)


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
		
		self.tree = ParameterTree(showHeader = False)
		self.splitterSubAdd.addWidget(self.tree)

		self.splitterSubView = QtGui.QSplitter()
		self.splitterSubView.setOrientation(QtCore.Qt.Vertical)
		self.splitterMain.addWidget(self.splitterSubView)

		
	# Adds a news window to add a new crystal next door
	def addCrystalParam(self):		
		self.params.addCrystalView(self.params)
		a = self.params.crystalList[
			self.params.param('Chemical Formula').value()].area
			
		self.dockAreaList[self.params.param('Chemical Formula').value()] = a
		self.splitterSubView.addWidget(a)
		self.params.param('Chemical Formula').setToDefault()
		self.params.param('Polytype').setToDefault()
		self.params.param('Temperature').setToDefault()
		self.params.param('Pressure').setToDefault()

	def crystalWindowRemove(self, param, child):
		self.dockAreaList[child.name()].close()
		del self.dockAreaList[child.name()]