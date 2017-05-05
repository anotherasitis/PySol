from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import matplotlib.pyplot as plt
import pyqtgraph.opengl as gl
import Energy as nrg
import numpy as np


kx=np.linspace(-2*np.pi/5,2*np.pi/5)
ky=np.linspace(-2*np.pi/5,2*np.pi/5)
kz=np.linspace(-2*np.pi/5,2*np.pi/5)
K1=np.array([ [kx], [ky] , [kz] ])
K2=np.array([ [kx], [np.linspace(0,0)] , [kz] ])
K3=np.array([ [kx], [np.linspace(0,0)] , [np.linspace(0,0)] ])

plv = np.array([[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]])
plotWidget = pg.plot(title="Nearly Free Electron Band Structure")
#FCC
m=1
hql=np.array([ [0,0,0],[1,1,1] ])
kpath=np.array([ [[0,0,0],[0.5,0.5,0.5]], [[0.5,0.5,0.5],[1,1,1]]])#[1,1,1], [3/2,1/2,1/2], [2,0,0] ])


for i in kpath[...,]:
	print(i[1][0])
	K=np.array([ [np.linspace(2*np.pi*i[1][0],2*np.pi*i[0][0])], [np.linspace(2*np.pi*i[1][1],2*np.pi*i[0][1])],[np.linspace(2*np.pi*i[1][2],2*np.pi*i[0][2])] ]) #-np.pi*(2*(i+1))
	Kpts=np.linspace(-np.pi,0)

	#Kgamma_X2=np.array([ [np.linspace(0,0)], [np.linspace(4*np.pi,2*np.pi)],[np.linspace(0,0) ]])
	#Kgamma_X2pts=np.linspace(0, 2*np.pi)


	#Kgamma_L= np.array([ [np.linspace(-1*np.pi,0)], [np.linspace(-1*np.pi,0)],[np.linspace(-(1)*np.pi,0)] ])
	#Kgamma_Lpts=np.linspace(-np.pi,0)

	#Kgamma_L2=np.array([ [np.linspace(-2*np.pi,-np.pi)], [np.linspace(-2*np.pi,-np.pi)],[np.linspace(-2*np.pi,-np.pi) ]])
	#Kgamma_L2pts=np.linspace(0, -np.pi)

	#Kgamma_U= np.array([ [np.linspace(0,0.5*np.pi)], [np.linspace(2*np.pi,2*np.pi)],[np.linspace(0,0.5*np.pi)] ])
	#Kgamma_Upts=np.linspace(2*np.pi,3*np.pi)

	Energy=np.array(nrg.nrg(plv,K,i[0][0],i[0][1],i[0][2]))
	#	nrg.nrg(plv,Kgamma_X2,i[0],i[1],i[2]) \
	#	, nrg.nrg(plv,Kgamma_L,i[0],i[1],i[2]),nrg.nrg(plv,Kgamma_L2,i[0],i[1],i[2]) \
	#	, nrg.nrg(plv,Kgamma_U,i[0],i[1],i[2])]) 
	

	plotWidget.plot(Kpts, Energy,pen=(1,1))
	#plotWidget.plot(Kgamma_X2pts, Energy[1],pen=(1,3))
	#plotWidget.plot(Kgamma_Lpts, Energy[2],pen=(2,3))
	#plotWidget.plot(Kgamma_L2pts, Energy[3],pen=(2,3))
	#plotWidget.plot(Kgamma_Upts, Energy[4],pen=(3,3))




pg.QtGui.QApplication.exec_()










