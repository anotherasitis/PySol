from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import matplotlib.pyplot as plt
import pyqtgraph.opengl as gl
import math
import Energy as nrg
import numpy as np
import latVectors as lv
import latPoints as lp
import Phase as phase

#This is the minimal requirements in order to plot the functional band structure, as a probe for mathematical errors

#Aaron: Notes for integration
#Atom1, Atom2: atomic number, number of valence orbital states
#plv= primitive lattice vectors, default fcc
#basis= dual basis for zinc blend ()
#Struct 'ZB' for  symmetry simplificiations, not explicitly used but was needed for the 

def LCAO(Atom1=[49,4], Atom2=[15,4],plv=np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]),basis=np.array([[0,0,0],[0.25,0.25,0.25]]),struct='ZB',latconst=1.8687E-10,bandPts = 5000):

	#This is the bond oreintations for the p orbitals, dont worry about adding this as input as this is fine to just exsist here as almost all bonding uses a p vec.

	pvec= np.array([[1,0,0],[0,1,0],[0,0,1]]) #p orbital bond vectors-> x,y,z for Lowdin orbitals
	#kplot=np.array([[0,0,0],[0,0,0],[0.5,0.5,0.5],[0,2,0],[0.5,2,0.5]]) #This is the set of symmetry vectors used for plotting, was automating more but not complete


	##Aaron note:
	#All these constants are good as is and wont change material to material

	#################################
	#Constants/Givens
	###############################
	Ry = -13.605 #Rydberg's number in eV
	a = latconst
	e = 1.60218e-19 #Electron Charge in C
	me = 9.10938E-31 #kg
	hbar = 1.05459E-34#joule form
	fineStruct = 0.0072973525664

	atoms = lp.latpts(basis, plv)
	bonds = lv.latVec(struct)

	#Nearest neighbor normalized vectors
	d_norm = np.array([(bonds[0][1] - bonds[0][0])/np.linalg.norm(bonds[0][1] - bonds[0][0]), \
		(bonds[0][2] - bonds[0][0])/np.linalg.norm(bonds[0][2] - bonds[0][0]), \
		(bonds[0][3] - bonds[0][0])/np.linalg.norm(bonds[0][3] - bonds[0][0]), \
		(bonds[0][4] - bonds[0][0])/np.linalg.norm(bonds[0][4] - bonds[0][0]) ])

	#Aaron: This is the list of bond energies that are hard to approximate (lines 66-70) do as you will

	E=np.array( [-11.37, -4.9, -4.9, -4.9, -17.44, -7.91, -7.91, -7.91], dtype=complex )
	Vpp_sigma = 3.44#bondE_approx
	Vpp_pi = -1.03#bondE_approx
	Vsp = 2.34
	Ess = -1.78

	#These use the values above, and are universal.
	Esp = np.dot(d_norm[0],pvec[0])*Vsp
	Exx = 1/3*Vpp_sigma+2/3*Vpp_pi
	Exy = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0]*np.dot(pvec[0],d_norm[0])) , (pvec[1] - d_norm[0]*np.dot(pvec[1],d_norm[0])))*Vpp_pi #1/3*Vpp_sigma-1/3*Vpp_pi

	#Zincblend symmetry consideration
	R1=np.array([bonds[0][2] - bonds[0][1],bonds[0][3] - bonds[0][1],bonds[0][4] - bonds[0][1] ])
	if struct=='ZB' :
		R2=-R1


	#for j in range(3):

		#kx=np.linspace(-(kplot[j][0]-kplot[j+1][0]) * np.pi/a , -(kplot[j+2][0]-kplot[j+1]) * np.pi/a ,bandPts)
		#ky=np.linspace(-(kplot[j][1]-kplot[j+1][1])*np.pi/a ,-(kplot[j+2][1]-kplot[j+1])*np.pi/a ,bandPts) #should be from 0-2*pi
		#kz=np.linspace(-(kplot[j][2]-kplot[j+1][2])*np.pi/a ,-(kplot[j+2][2]-kplot[j+1])*np.pi/a ,bandPts)
		#Kpts=np.linspace(j,j+1,bandPts)
		#K1=np.array([ kx , ky, kz ])

	#Region 1
	BandE = np.zeros((8 , bandPts))
	kx = np.linspace(0 , 0*np.pi/a,bandPts)
	ky = np.linspace(0 , 2*np.pi/a,bandPts)
	kz = np.linspace(0 , 0*np.pi/a,bandPts)
	K1 = np.array([ kx , ky , kz ])
	Kpts = np.linspace(0 , 1 , bandPts)
	for i in range(bandPts):
			K=K1[...,i]
			g=[0,0,0,0]

			g1=phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0],'s')
			g2= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0])
			g3= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[1])
			g4= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[2])
			#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))

			g1_conj= np.conjugate(g1)
			g2_conj= np.conjugate(g2)
			g3_conj= np.conjugate(g3)
			g4_conj= np.conjugate(g4) 

			Hamil=np.zeros((8,8),dtype=complex)

			Hamil=np.matrix([ [E[0],0,0,0,Ess*g1,Esp,Esp,Esp], \
				[0,E[1],0,0,-Esp*g2,Exx*g1,Exy*g4,Exy*g3], \
				[0,0,E[2],0,-Esp*g3,Exy*g4,Exx*g1,Exy*g2], \
				[0,0,0,E[3],-Esp*g4,Exy*g3,Exy*g2,Exx*g1], \
				[Ess*g1_conj,-Esp*g2_conj,-Esp*g3_conj,-Esp*g4_conj,E[4],0,0,0],  \
				[Esp*g2_conj,Exx*g1_conj,Exy*g4_conj,Exy*g3_conj,0,E[5],0,0], \
				[Esp*g3_conj,Exy*g4_conj,Exx*g1_conj,Exy*g2_conj,0,0,E[6],0], \
				[Esp*g4_conj,Exy*g3_conj,Exy*g2_conj,Exx*g1_conj,0,0,0,E[7]] ], dtype=complex)

			BandE[...,i]=np.sort(np.linalg.eigvals(Hamil))

	#Region 2
	BandE2 = np.zeros((8 , bandPts))
	kx = np.linspace(0 , 1*np.pi/a , bandPts)
	ky = np.linspace(0 , 1*np.pi/a , bandPts) 
	kz = np.linspace(0 , 1*np.pi/a , bandPts)
	K1 = np.array([ kx , ky , kz ])
	Kpts2 = np.linspace(0 , -1 , bandPts)
	for i in range(bandPts):
			K=K1[...,i]

			g=[0,0,0,0]

			g1=phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0],'s')
			g2= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0])
			g3= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[1])
			g4= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[2])
			#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))

			g1_conj= np.conjugate(g1)
			g2_conj= np.conjugate(g2)
			g3_conj= np.conjugate(g3)
			g4_conj= np.conjugate(g4)

			Hamil=np.zeros((8,8),dtype=complex)

			Hamil=np.matrix([ [E[0],0,0,0,Ess*g1,Esp,Esp,Esp], \
				[0,E[1],0,0,-Esp*g2,Exx*g1,Exy*g4,Exy*g3], \
				[0,0,E[2],0,-Esp*g3,Exy*g4,Exx*g1,Exy*g2], \
				[0,0,0,E[3],-Esp*g4,Exy*g3,Exy*g2,Exx*g1], \
				[Ess*g1_conj,-Esp*g2_conj,-Esp*g3_conj,-Esp*g4_conj,E[4],0,0,0],  \
				[Esp*g2_conj,Exx*g1_conj,Exy*g4_conj,Exy*g3_conj,0,E[5],0,0], \
				[Esp*g3_conj,Exy*g4_conj,Exx*g1_conj,Exy*g2_conj,0,0,E[6],0], \
				[Esp*g4_conj,Exy*g3_conj,Exy*g2_conj,Exx*g1_conj,0,0,0,E[7]] ], dtype=complex)

			BandE2[...,i]=np.sort(np.linalg.eigvals(Hamil))

	#Region 3
	BandE3 = np.zeros((8,bandPts))
	kx2 = np.linspace(0 , 0.5*np.pi/a , bandPts)
	ky2 = np.linspace(2*np.pi/a , 2*np.pi/a , bandPts) 
	kz2 = np.linspace(0,0.5*np.pi/a , bandPts)
	K2 = np.array([ kx2 , ky2 , kz2 ])
	Kpts3=np.linspace(1 , 1.5 , bandPts)
	for i in range(bandPts):
			K=K2[...,i]

			g=[0,0,0,0]

			g1=phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0],'s')
			g2= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0])
			g3= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[1])
			g4= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[2])
			#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))

			g1_conj= np.conjugate(g1)
			g2_conj= np.conjugate(g2)
			g3_conj= np.conjugate(g3)
			g4_conj= np.conjugate(g4)

			Hamil=np.zeros((8,8),dtype=complex)

			Hamil=np.matrix([ [E[0],0,0,0,Ess*g1,Esp,Esp,Esp], \
				[0,E[1],0,0,-Esp*g2,Exx*g1,Exy*g4,Exy*g3], \
				[0,0,E[2],0,-Esp*g3,Exy*g4,Exx*g1,Exy*g2], \
				[0,0,0,E[3],-Esp*g4,Exy*g3,Exy*g2,Exx*g1], \
				[Ess*g1_conj,-Esp*g2_conj,-Esp*g3_conj,-Esp*g4_conj,E[4],0,0,0],  \
				[Esp*g2_conj,Exx*g1_conj,Exy*g4_conj,Exy*g3_conj,0,E[5],0,0], \
				[Esp*g3_conj,Exy*g4_conj,Exx*g1_conj,Exy*g2_conj,0,0,E[6],0], \
				[Esp*g4_conj,Exy*g3_conj,Exy*g2_conj,Exx*g1_conj,0,0,0,E[7]] ], dtype=complex)

			BandE3[...,i]=np.sort(np.linalg.eigvals(Hamil))

	#Region 4
	BandE4 = np.zeros((8 , bandPts))
	kx3 = np.linspace(0.5*np.pi/a , 0 , bandPts)
	ky3 = np.linspace(2*np.pi/a , 0 , bandPts)
	kz3 = np.linspace(0.5*np.pi/a , 0 , bandPts)
	K3 = np.array([ kx3 , ky3, kz3 ])
	Kpts4 = np.linspace(1.5 , 2.5 , bandPts)
	for i in range(bandPts):
			K=K3[...,i]

			g=[0,0,0,0]

			g1=phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0],'s')
			g2= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0])
			g3= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[1])
			g4= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[2])
			#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))

			g1_conj= np.conjugate(g1)
			g2_conj= np.conjugate(g2)
			g3_conj= np.conjugate(g3)
			g4_conj= np.conjugate(g4)

			Hamil=np.zeros((8,8),dtype=complex)

			Hamil=np.matrix([ [E[0],0,0,0,Ess*g1,Esp,Esp,Esp], \
				[0,E[1],0,0,-Esp*g2,Exx*g1,Exy*g4,Exy*g3], \
				[0,0,E[2],0,-Esp*g3,Exy*g4,Exx*g1,Exy*g2], \
				[0,0,0,E[3],-Esp*g4,Exy*g3,Exy*g2,Exx*g1], \
				[Ess*g1_conj,-Esp*g2_conj,-Esp*g3_conj,-Esp*g4_conj,E[4],0,0,0],  \
				[Esp*g2_conj,Exx*g1_conj,Exy*g4_conj,Exy*g3_conj,0,E[5],0,0], \
				[Esp*g3_conj,Exy*g4_conj,Exx*g1_conj,Exy*g2_conj,0,0,E[6],0], \
				[Esp*g4_conj,Exy*g3_conj,Exy*g2_conj,Exx*g1_conj,0,0,0,E[7]] ], dtype=complex)

			BandE4[...,i]=np.sort(np.linalg.eigvals(Hamil))

	#Plotting
	plotWidget = pg.plot(title="Band Structure")
	for i in range(8):
		plotWidget.plot(Kpts , BandE[i,...] , pen=(i,8))
		plotWidget.plot(Kpts2 , BandE2[i,...] , pen=(i,8))
		plotWidget.plot(Kpts3 , BandE3[i,...] , pen=(i,8))
		plotWidget.plot(Kpts4 , BandE4[i,...] , pen=(i,8))


	pg.QtGui.QApplication.exec_()



