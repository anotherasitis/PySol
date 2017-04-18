from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
import re
import csv
import crystalViewBase
import pyqtgraph as pg
import pyqtgraph.exporters
import pyqtgraph.opengl as gl

class crytalParamInitialize(pTypes.GroupParameter):

	def __init__(self, **kwds):
		self.crystalList = {}
		self.chemicals = []
		self.chemNum = {}
		defs = dict(name = 'params', type = 'group',children =[ 
				dict(name = 'Chemical Formula', type = 'str', value = '', default = ''),
				dict(name = 'Polytype', type = 'str', value = '', default = ''),
				dict(name = 'Temperature', type = 'float', value = 293, default = 293, 
					siPrefix = True, suffix = 'K'),
	
				dict(name = 'Pressure', type = 'float', value = 101, default = 101, 
					siPrefix = True, suffix = 'kPa'),
	
				dict(name = 'Add Crystal', type = 'action'),
				dict(name = 'Crystals', type = 'group', removable = False, visible = True, enabled = False),
				])

		pTypes.GroupParameter.__init__(self, **defs)
		self.param('Crystals').sigChildRemoved.connect(self.crystalRemoved)
		self.param('Chemical Formula').sigTreeStateChanged.connect(self.isValidChem)

	def addCrystalView(self, paramsToApply):
		a = crystalViewBase.crystalViewBase(paramsToApply)
		self.crystalList[paramsToApply.param('Chemical Formula').value()] = a
		self.param('Crystals').addChild(a)

	def crystalRemoved(self, param, child):
		del self.crystalList[child.name()]

	def isValidChem(self):
		self.chemicals[self.param('Chemical Formula').value()
			] = re.findall('[A-Z][^A-Z]*', self.param('Chemical Formula').value())

		elementDict = {}
		with open('elementlist.csv') as csvfile:
			element = csv.reader(csvfile)
			for i in element:
				elementDict[i[1]] = [i[0], i[2]]

		self.chemNum[self.param('Chemical Formula').value()] = [
			elementDict[self.chemicals[self.param('Chemical Formula').value()][0]], 
			elementDict[self.chemicals[self.param('Chemical Formula').value()][1]]]
		
		print(self.chemNum, self.chemicals)