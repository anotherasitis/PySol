from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
import graphBase
import crystalViewBase
import pyqtgraph as pg
import pyqtgraph.exporters
import pyqtgraph.opengl as gl

class crystalParamBase(QtGui.QWidget):

	def __init__(self, graphBaseWin):
		self.splitterSubSubParam = QtGui.QSplitter()
		self.splitterSubSubParam.setOrientation(QtCore.Qt.Vertical)
		self.tree = ParameterTree(showHeader=False)
		self.newCrystalView = QtGui.QPushButton('Show Crystal Structure', self)
		self.newCrystalView.clicked.connect(self.addCrystalView)
		self.splitterSubSubParam.addWidget(self.tree)
		self.splitterSubSubParam.addWidget(self.newCrystalView)
		graphBaseWin.splitterSubAdd.addWidget(self.splitterSubSubParam)

		self.crystalView=[]

	def addCrystalView(self):
		self.crystalView.append(crystalViewBase.CrystalViewBase(grapBaseWin, self))
