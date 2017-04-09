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

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.setBackgroundColor('k')
w.show()
w.setWindowTitle('Structure')
w.setCameraPosition(distance=3, azimuth=-280)

########################################### General Properties
transp=1
scl=1
numLat=2
firOrg=np.array([0,0,0])

########################################### Grid Properties
grids=[]
rotArr=np.array([0,0,0])
grdLbl=['X-Axis','Y-Axis','Z-Axis']

########################################### Box Properties
bxs=[]
lbl=[]
bxSdLen=1
linewidth=3
bxOrPar=np.empty([numLat,3])

########################################### Crystal Properties
strt=[]
xtlType='zinc'
xtlView='std'
numDiffAt=2
res=20

########################################### Plane Properties
plns=[]##############doesnt work yet
showPln=False
plnRes=res*7
plnTransp=transp/3
plnOr=np.array([1,1,0])

########################################### Truncated Octahedron Properties
octHdr=[]
octTransp=transp/3

########################################### Setting up Origins
for i in range(numLat):
	if xtlView=='std':
		if i>0:
			bxOrPar[i]=bxOrPar[i-1]+1

		else:
			bxOrPar[i]=firOrg

	elif xtlView=='rcp':
		if i>0:
			bxOrPar[i]=bxOrPar[i-1]+0.5

		else:
			bxOrPar[i]=firOrg

########################################### Make Grids
for indx, i in enumerate(bxOrPar.T):
	rotArr[indx]=1
	grids.append(mkGds.mkGds(i,bxSdLen,scl))
	grids[indx].rotate(270+90*indx, rotArr[2], rotArr[0], rotArr[1])
	# lbl.append(pg.LabelItem(text=grdLbl[indx],parent=grids[indx]))
	rotArr=np.array([0,0,0])


for i in bxOrPar:
	########################################### Make Boxes
	bxs.append(mkBx.mkBx(i[0], i[1], i[2],linewidth,transp,scl,bxSdLen))
	########################################### Make Crystal Lattices
	strt.append(mkXtlSt.mkXtlSt(xtlType,xtlView,numDiffAt,res,i,bxSdLen,scl,transp,linewidth))
	########################################## Make Planes
	if showPln:
		plns.append(mkPlns.mkPlns(plnOr,i,bxSdLen,scl,plnRes,plnTransp))
	
	########################################### Make Truncated Octahedron
	if xtlView=='rcp':
		octHdr.append(mkOct.mkOctHdr(i,bxSdLen,scl,octTransp))

########################################### Plot Everything
axs=gl.GLAxisItem(glOptions='opaque')
axs.setSize(x=scl,y=scl,z=scl)
# axs.translate(fullD[0],fullD[1],fullD[2])
w.addItem(axs)
fullD=np.zeros((3,1))
for indx, i in enumerate(bxOrPar.T):
	dir=-np.sign(i.min())
	if dir==0:
		dir=-1
	
	fullD[indx]=dir*((bxSdLen+i.max())+i.min())/2

for i in bxs:
	for j in i:
		j.translate(fullD[0],fullD[1],fullD[2])
		w.addItem(j)

for i in grids:
	i.translate(fullD[0],fullD[1],fullD[2])
	w.addItem(i)

for i in strt:
	for j in i:
		j.translate(fullD[0],fullD[1],fullD[2])
		w.addItem(j)

if xtlView=='rcp':
	for i in octHdr:
		i.translate(fullD[0],fullD[1],fullD[2])
		w.addItem(i)

if showPln:
	for i in plns:
		i.translate(fullD[0],fullD[1],fullD[2])
		w.addItem(i)

w.grabFrameBuffer().save('try1.bmp')

if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()