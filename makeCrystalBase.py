from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.parametertree import types as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.parametertree import ParameterItem, registerParameterType
import FermiSurf
import crystalStruct
import numpy as np
import itertools as itTl
import pyqtgraph as pg
import makeBox as mkBx
import pyqtgraph.exporters
import makeGrids as mkGds
import pyqtgraph.opengl as gl
import makePlanes as mkPlns
import makeOcthedron as mkOct
import symmetryLines as symLns
import makeCrystalStruct as mkXtlSt

class makeCrystals():

	def __init__(self, crystData, latGraphType):
		self.w = gl.GLViewWidget()
		self.w.setBackgroundColor('k')
		self.w.setCameraPosition(distance=3, azimuth=-280)

		self.transp=1
		self.scl=1
		self.numLat=crystData.bounds
		self.firOrg=np.array([0,0,0])

		########################################### Grid Properties
		self.grids=[]
		self.rotArr=np.array([0,0,0])
		self.grdLbl=['X-Axis','Y-Axis','Z-Axis']

		########################################### Box Properties
		self.bxs=[]
		self.lbl=[]
		self.bxSdLen=1
		self.linewidth=3
		self.bxOrPar=[]

		########################################### Crystal Properties
		self.strt=[]
		self.xtlType=crystData.polyType
		self.xtlView=latGraphType
		self.numDiffAt=len(crystData.atms)
		self.res=20

		########################################### Plane Properties
		self.plns=[]##############doesnt work yet
		self.showPln=False
		self.plnRes=self.res*7
		self.plnTransp=self.transp/3
		self.plnOr=np.array([1,1,0])

		########################################### Truncated Octahedron Properties
		# if latGraphType=='Direct Lattice' or latGraphType=='Reciprocal Lattice':
	
	def createOrAdd(self,clickedBut):
		print('make'+(clickedBut.replace(' ','').split('.', 1))[-1])
		getattr(self,'make'+(clickedBut.replace(' ','').split('.', 1))[-1])()
		

	def makeDirectLattice(self):
		self.makeLatItems()

	def makeReciprocalLattice(self):
		self.makeLatItems()

	def makeLatItems(self):
		boxCorn=np.linspace(self.firOrg.min(),self.numLat.max()-1,num=self.numLat.max()-self.firOrg.min())
		boxPos=np.array(list(itTl.product(boxCorn, repeat=3)))
		z=np.where(np.all([
			np.less(boxPos,self.numLat).all(axis=1),
			np.greater_equal(boxPos,self.firOrg).all(axis=1)
			],axis=0))

		self.bxOrPar=boxPos[z]
		print(self.bxOrPar)
		for indx, i in enumerate(self.bxOrPar.T):
			self.rotArr[indx]=1
			self.grids.append(mkGds.mkGds(i,self.bxSdLen,self.scl))
			self.grids[indx].rotate(270+90*indx, self.rotArr[2], self.rotArr[0], self.rotArr[1])
			# lbl.append(pg.LabelItem(text=grdLbl[indx],parent=grids[indx]))
			self.rotArr=np.array([0,0,0])

		for i in self.bxOrPar:
			self.bxs.append(mkBx.mkBx(i[0], i[1], i[2],self.linewidth,self.transp,self.scl,self.bxSdLen))
			self.strt.append(mkXtlSt.mkXtlSt(self.xtlType,self.xtlView,self.numDiffAt,self.res,
				i,self.bxSdLen,self.scl,self.transp,self.linewidth))

			if self.showPln:
				self.plns.append(mkPlns.mkPlns(self.plnOr,i,self.bxSdLen,self.scl,
					self.plnRes,self.plnTransp))

		self.axs=gl.GLAxisItem(glOptions='opaque')
		self.axs.setSize(x=self.scl,y=self.scl,z=self.scl)
		self.w.addItem(self.axs)
		self.fullD=np.zeros((3,1))
		for indx, i in enumerate(self.bxOrPar.T):
			dir=-np.sign(i.min())
			if dir==0:
				dir=-1
			
			self.fullD[indx]=dir*((self.bxSdLen+i.max())+i.min())/2

		for i in self.bxs:
			for j in i:
				j.translate(self.fullD[0],self.fullD[1],self.fullD[2])
				self.w.addItem(j)

		for i in self.grids:
			i.translate(self.fullD[0],self.fullD[1],self.fullD[2])
			self.w.addItem(i)

		for i in self.strt:
			for j in i:
				j.translate(self.fullD[0],self.fullD[1],self.fullD[2])
				self.w.addItem(j)

		if self.showPln:
			for i in self.plns:
				i.translate(self.fullD[0],self.fullD[1],self.fullD[2])
				self.w.addItem(i)

	def makeFirstBrillouinZone(self):
		self.octHdr = []
		self.octTransp = 0.6
		for i in self.bxOrPar:
			a = mkOct.mkOctHdr(i,self.bxSdLen,self.scl,self.octTransp)
			a.translate(self.fullD[0],self.fullD[1],self.fullD[2])
			self.octHdr.append(a)
			symline=symLns.addSymLns(i,self.scl,self.bxSdLen,self.octTransp)
			for j in symline:
				j.translate(self.fullD[0],self.fullD[1],self.fullD[2])
				self.octHdr.append(j)

		for i in self.octHdr:
			self.w.addItem(i)

	def makeFermiSurface(self):
		self.frmSurf = []
		self.frmTransp = 0.6
		for i in self.bxOrPar:
			a=FermiSurf.fermiSurf()
			a.translate(((self.bxSdLen/2)+i[0]), ((self.bxSdLen/2)+i[1]), ((self.bxSdLen/2)+i[2]))
			a.translate(self.fullD[0]-0.5*self.scl,self.fullD[1]-0.5*self.scl,self.fullD[2]-0.5*self.scl)
			self.frmSurf.append(a)

		for i in self.frmSurf:
			self.w.addItem(i)
