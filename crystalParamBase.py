from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
import crystalViewBase
import pyqtgraph as pg
import pyqtgraph.exporters
import pyqtgraph.opengl as gl

class crytalParamInitialize(pTypes.GroupParameter):

	def __init__(self, **kwds):

		self.crystalBase = crystalParamBase()
		defs = dict(name = 'params', type = 'group',
			children = [
			dict(name = 'Chemical Formula', type = 'str', value = '', default = ''),
			dict(name = 'Polytype', type = 'str', value = '', default = ''),
			dict(name = 'Temperature', type = 'float', value = 293, default = 293, 
				siPrefix = True, suffix = 'K'),

			dict(name = 'Pressure', type = 'float', value = 101, default = 101, 
				siPrefix = True, suffix = 'kPa'),

			dict(name = 'Add Crystal', type = 'action'),
			self.crystalBase,
			])

		pTypes.GroupParameter.__init__(self, **defs)

class crystalParamBase(pTypes.GroupParameter):

	def __init__(self, **kwds):
		pTypes.GroupParameter.__init__(self, name = 'Crystals')

	def addCrystalView(self, paramsToApply):
		self.addChild(crystalViewBase.crystalViewBase(paramsToApply))