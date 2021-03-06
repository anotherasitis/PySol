from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
import crystalStruct
import numpy as np
import pyqtgraph as pg
import makeCrystalBase
import pyqtgraph.exporters
import pyqtgraph.opengl as gl
# import itertools as itTl
# import makeBox as mkBx
# import makeGrids as mkGds
# import makePlanes as mkPlns
# import makeOcthedron as mkOct
# import makeCrystalStruct as mkXtlSt

class crystalViewBase(pTypes.GroupParameter):

	def __init__(self, paramsToApply, chemicals, chemNum, primLatVec):
		self.dockList = {}
		self.graphicViewObj = {}
		defs = dict(name = paramsToApply.param('Chemical Formula').value(),
			removable = True, children = [
			dict(name = 'Polytype', type = 'str', 
				value = paramsToApply.param('Polytype').value(), readonly = True),

			dict(name = 'Temperature', type = 'float', 
				value = paramsToApply.param('Temperature').value(), 
				readonly = True, siPrefix = True, suffix = 'K'),

			dict(name = 'Pressure', type = 'float',
				value = paramsToApply.param('Pressure').value(),
				readonly = True, siPrefix = True, suffix = 'Pa'),
			
			dict(name = 'Display...', children = [
			 	dict(name = 'Direct Lattice', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Dimension to Display (X)', type = 'int', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Y)', type = 'int', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Z)', type = 'int', value = 1,
			 			default = 1)
			 		]),

			 	dict(name = 'Reciprocal Lattice', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Dimension to Display (X)', type = 'int', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Y)', type = 'int', value = 1,
			 			default = 1),

			 		dict(name = 'Crystal Dimension to Display (Z)', type = 'int', value = 1,
			 			default = 1),

			 		dict(name = 'Fermi Surface', type = 'bool', value = False, default = False),
			 		dict(name = 'First Brillouin Zone', type = 'bool', value = False, default = False)
			 		]),

			 	dict(name = 'Show Planes in...', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Crystal Lattice', type = 'bool', value = False, default = False),
					dict(name = 'Reciprocal Lattice', type = 'bool', value = False, default = False),
			 		dict(name = 'Axis', type = 'int', value = 000, default = 000) 
			 		]),

			 	dict(name = 'X-Ray Diffraction Pattern', type = 'bool', value = False, default = False,
			 		children = [
			 		dict(name = 'Axis', type = 'int', value = 000, default = 000) 
			 			]),

			 	dict(name = 'Phonon Dispersion Curve', type = 'bool', value = False, default = False),
			 	dict(name = 'Electronic Band Structure', children = [
			 		dict(name = 'LCAO Model',type = 'bool', value = False, default = False),
			 		#dict(name = 'NFEM Model',type = 'bool', value = False, default = False),
			 		])
		 		]),
		 	])
		pTypes.GroupParameter.__init__(self, **defs)
		self.paramDict = {
			'Polytype' : paramsToApply.param('Polytype').value(),
			'Temperature' : paramsToApply.param('Temperature').value(),
			'Pressure' : paramsToApply.param('Pressure').value(),
			'atms' : chemicals,
			'chemNum' : chemNum,
			}

		self.crystalStruct = crystalStruct.crystalStruct(self.paramDict, np.array(primLatVec).astype(float))
		# self.crystGraphBase = makeCrystalBase.makeCrystals(self.crystalStruct)
		self.area = DockArea()
		self.param('Display...').sigTreeStateChanged.connect(self.displayChecked)
	
	def displayChecked(self, param, changes):
		for param, change, data in changes:
			path = self.param('Display...').childPath(param)
			if path is not None:
				childName = '.'.join(path)
			
			else:
				childName = param.name()
			
			if data and isinstance(data, bool):
				if childName == 'Direct Lattice' or childName == 'Reciprocal Lattice':
					self.crystalStruct.bounds = np.array([
						self.param('Display...').param(childName).param( 'Crystal Dimension to Display (X)').value(),
						self.param('Display...').param(childName).param( 'Crystal Dimension to Display (Y)').value(),
						self.param('Display...').param(childName).param( 'Crystal Dimension to Display (Z)').value()])
				
				self.crystalStruct.reInitalizeAllDat()
				if param.parent().name() == 'Reciprocal Lattice':
					self.graphicViewObj['Reciprocal Lattice'].createOrAdd(childName)

				else:
					self.graphicViewObj[childName] = makeCrystalBase.makeCrystals(self.crystalStruct, childName)
					self.graphicViewObj[childName].createOrAdd(childName)
					if param.parent().name() == 'Electronic Band Structure':
						self.addDock(self.param('Display...').parent().name()
							+' '+childName, self.graphicViewObj[childName].lcaoBndStruct)

					else:
						self.addDock(self.param('Display...').parent().name()
							+' '+childName, self.graphicViewObj[childName].w)

			elif not data and isinstance(data, bool):			
				if param.parent().name() == 'Reciprocal Lattice':
					pass

				else:
					self.removeDock(self.param('Display...').parent().name()
						+' '+childName)
					del self.graphicViewObj[childName]
					if param.hasChildren():
						for i in param.children():
							i.setToDefault()


	def addDock(self, name, w):
		d = Dock(name)
		d.addWidget(w)
		self.dockList[name] = d
		self.area.addDock(d)

	def removeDock(self, name):
		self.dockList[name].close()
		del self.dockList[name]