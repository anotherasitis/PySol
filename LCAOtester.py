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

#################################
#Constants/Givens
###############################
bandPts=500
Ry=-13.605 #Rydberg's number in eV
#lattice constant
a=1.8687E-10 #in Meters
e=1.60218e-19
me=9.10938E-31 #kg
hbar=1.05459E-34#
fineStruct=0.0072973525664
pvec= np.array([[1,0,0],[0,1,0],[0,0,1]]) #p orbital bond vectors-> x,y,z for Lowdin orbitals

##############################################################################################
######################LCAO trial run for indium phosphide#####################################
##############################################################################################

###################
#Indium information
###################
In_atomicNum=49
In_valenceE=3
In_states=4
In_valenceN=5
In_orbitals=np.array([ ['s'],['p'] ])

#######################
#Phosphorus information
#######################
P_atomicNum=15
P_valenceE=5
P_valenceN=3
P_states=4
P_orbitals=np.array([ ['s'],['p'] ])

#Using the lattice functions to define all needed variables throughout the program: lattice points, nearest neighbor vectors, unit bond vectors etc
atoms = lp.latpts(np.array([[0,0,0],[0.25,0.25,0.25]]), np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]))
bonds = lv.latVec('ZB')


Atom1_R=np.array([bonds[0][2]-bonds[0][1],bonds[0][3]-bonds[0][1],bonds[0][4]-bonds[0][1] ])*a
Atom2_R=np.array([(bonds[33.25][2]-bonds[33.25][1]),(bonds[33.25][3]-bonds[33.25][1]),(bonds[33.25][4]-bonds[33.25][1]) ])*a


d_norm=np.array([(bonds[0][1]-bonds[0][0])/np.linalg.norm(bonds[0][1]-bonds[0][0]), \
	(bonds[0][2]-bonds[0][0])/np.linalg.norm(bonds[0][2]-bonds[0][0]), \
	(bonds[0][3]-bonds[0][0])/np.linalg.norm(bonds[0][3]-bonds[0][0]), \
	(bonds[0][4]-bonds[0][0])/np.linalg.norm(bonds[0][4]-bonds[0][0]) ])
#np.array([-(bonds[33.25][2]-bonds[33.25][1]), -(bonds[33.25][3]-bonds[33.25][1]), -(bonds[33.25][4]-bonds[33.25][1]) ])
print(d_norm)
#################################################################################
#Constructing the Hamiltonian
#################################################################################

m=In_states+P_states

########################################
#Pure orbital Approixmate energy states#
########################################
#Simpliest form
#No Zeff implimented
#Units of electron volts
#sommerfield dirac approximation

orbitE_pure=np.linspace(0,1,In_states+P_states)

for i in range(In_states):
	if i==0:
		j=0
	else:
		j=1

	sigma=(j+0.5)*(1-math.sqrt((1-(In_atomicNum*fineStruct/(j+0.5))**2)))
	fnj=1/math.sqrt(1+(In_atomicNum*fineStruct/(In_valenceN-sigma))**2)
	orbitE_pure[i]= 2/(fineStruct**2)*(fnj-1)

for i in range(P_states):
	if i==0:
		j=0
	else:
		j=1
		
	sigma=(j+0.5)*(1-math.sqrt((1-(P_atomicNum*fineStruct/(j+0.5))**2)))
	fnj=1/math.sqrt(1+(P_atomicNum*fineStruct/(P_valenceN-sigma))**2)
	orbitE_pure[i+In_states]= 2/(fineStruct**2)*(fnj-1)


ro=((me*e*e)/(hbar*hbar)*np.linalg.norm(np.array([0.25,0.25,0.25])))
bondE_approx=2*(1+ro)*np.exp(-ro)
orbitE_pure=orbitE_pure/10

print(orbitE_pure)
orbitE_pure=np.array([-11.37,-4.9,-4.9,-4.9,-17.44,-7.91,-7.91,-7.91])
print(orbitE_pure)

Ess=-1.78#bondE_approx

#########################
#Esp and Esp_conj
#########################
Esp=np.linspace(0,1,6)
Esp_conj=np.linspace(0,1,6)

#Vsp
#Using above approx
Vsp=2.34#bondE_approx

#Esp
Esp[0]=np.dot(d_norm[0],pvec[0])*Vsp
Esp[1]=np.dot(d_norm[0],pvec[1])*Vsp
Esp[2]=np.dot(d_norm[0],pvec[2])*Vsp

Esp[3]=-1*np.dot(d_norm[0],pvec[0])*Vsp
Esp[4]=-1*np.dot(d_norm[0],pvec[1])*Vsp
Esp[5]=-1*np.dot(d_norm[0],pvec[2])*Vsp
#print(Esp)


#Esp_conj
Esp_conj[0]=np.dot(d_norm[0],pvec[0])*Vsp
Esp_conj[1]=np.dot(d_norm[0],pvec[1])*Vsp
Esp_conj[2]=np.dot(d_norm[0],pvec[2])*Vsp

Esp_conj[3]=-1*np.dot(d_norm[0],-pvec[0])*Vsp
Esp_conj[4]=-1*np.dot(d_norm[0],-pvec[1])*Vsp
Esp_conj[5]=-1*np.dot(d_norm[0],-pvec[2])*Vsp

########################################
#px-px etc bond interactions for Exx, Eyy, Ezz
########################################

Epp = np.linspace(0,1,3)

Vpp_sigma = 3.44#bondE_approx
Vpp_pi = -1.03#bondE_approx

print(Vpp_pi)
#Exx
Epp[0] = np.array([np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[0])*Vpp_sigma \
	+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[0] - d_norm[0] * np.dot(pvec[0],d_norm[0]) ) ) * Vpp_pi])

#Eyy
Epp[1] = np.array([np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
	+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[1] - d_norm[0] * np.dot(pvec[1],d_norm[0]) ) ) * Vpp_pi])

#Ezz
Epp[2] = np.array([np.dot(d_norm[0],pvec[2])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
	+ np.dot((pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0])),(pvec[2] - d_norm[0] * np.dot(pvec[2],d_norm[0]) ) ) * Vpp_pi])




#study about k=0 for both X and L points
kx=np.linspace(0,0*np.pi/a,bandPts)
ky=np.linspace(0,2*np.pi/a,bandPts) #should be from 0-2*pi
kz=np.linspace(0,0*np.pi/a,bandPts)
K1=np.array([ kx , ky, kz ])
Kpts_L=np.linspace(0,1,bandPts)
BandE=np.zeros((In_states+P_states,bandPts))

print(bonds[0][1:4])

for k in range(bandPts):

	#################################
	#Ess and Ess_Conj
	#################################

	K=K1[...,k]

	
	g=[0,0,0,0]
	g_conj=[0,0,0,0]
	g[0]=phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0],'s')
	g[1]= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[0])
	g[2]= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[1])
	g[3]= phase.g(bonds[0][1:4]*a,K,d_norm,pvec[2])
	#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))
	g_conj[0]=phase.g(-bonds[0][1:4]*a,K,d_norm,pvec[0],'s')# 1 + np.exp(-1j*np.dot(K, Atom2_R[0])) + np.exp(-1j*np.dot(K, Atom2_R[1])) + np.exp(-1j*np.dot(K, Atom2_R[2]))
	g_conj[1]= phase.g(-bonds[0][1:4]*a,K,d_norm,pvec[0])
	g_conj[2]= phase.g(-bonds[0][1:4]*a,K,d_norm,pvec[1])
	g_conj[3]= phase.g(-bonds[0][1:4]*a,K,d_norm,pvec[2])


	######################################################
	#px-py cross terms bond interactions for Exy, Exz, Eyz
	######################################################

	Epp_cross=np.linspace(0,1,6,dtype=complex)
	#Exy
	Epp_cross[0] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Exz
	Epp_cross[1] = (np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Eyz
	Epp_cross[2] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]
	#Eyx
	Epp_cross[3] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Ezx
	Epp_cross[4] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Ezy
	Epp_cross[5] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]


	#########################################################
	#Populating Hamiltonian

	Hamil=np.zeros((m,m),dtype=complex)

	#########################################################
	#######Pure states#######

	for i in range(m):
		Hamil[i,i]=orbitE_pure[i]

	#Atom2_1 coupling matrix
	coup2_1=np.zeros((P_states,In_states), dtype=complex)
	sp_conj_counter=0
	pp_counter=0

	for i in range(P_states):
		for j in range(In_states):
			if i==0 and j==0 :
				coup2_1[i,j]= g_conj[0]
			elif i==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif i==j :
				coup2_1[i,j]=Epp[i-1]*g_conj[0]
			else:
				coup2_1[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1

	#Atom1_2 coupling matrix
	coup1_2=np.zeros((In_states,P_states), dtype=complex)
	sp_counter=0
	pp_counter=0

	for i in range(In_states):
		for j in range(P_states):
			if i==0 and j==0 :
				coup1_2[i,j]= g[0]
			elif i==0 :
				coup1_2[i,j]= Esp[sp_counter] *g[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup1_2[i,j]= Esp[sp_counter] *g[j]
				sp_counter= sp_counter+1
			elif i==j :
				coup1_2[i,j]=Epp[i-1]*g[0]
			else:
				coup1_2[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1
	### Hamil final ####
	for i in range(In_states):
		for j in range(P_states):
			Hamil[i+In_states,j]=coup1_2[i,j]
			Hamil[i,j+P_states]=coup2_1[i,j]


	Hamil_conj=np.matrix.conjugate(Hamil)
	#print(Hamil)
	#print(Hamil_conj)
	#print(Hamil*Hamil_conj)
	#print(Hamil.real)
	#BandE[...,k]=np.linalg.eigvals(Hamil)#
	BandE[...,k]=np.linalg.eigvals(np.absolute(Hamil))

	#print(np.linalg.eigvals(Hamil))


plotWidget = pg.plot(title="Band Structure")
for i in range(8):
	plotWidget.plot(Kpts_L,BandE[i,...], pen=(i,8))

plotWidget.plot(Kpts_L,BandE[0,...], pen=(8,8))

print(Hamil)


#########################################################################
#########################################################################
#########################################################################
#########################################################################

kx=np.linspace(0,np.pi/a,bandPts)
ky=np.linspace(0,np.pi/a,bandPts)
kz=np.linspace(0,np.pi/a,bandPts)
K1=np.array([ kx , ky, kz ])
Kpts_X=np.linspace(0,-1,bandPts)
BandE2=np.zeros((In_states+P_states,bandPts))


for k in range(bandPts):

	#################################
	#Ess and Ess_Conj
	#################################

	K=K1[...,k]

	
	g=[0,0,0,0]
	g_conj=[0,0,0,0]
	g[0]=phase.g(Atom1_R,K,d_norm,pvec[0],'s')
	g[1]= phase.g(Atom1_R,K,d_norm,pvec[0])
	g[2]= phase.g(Atom1_R,K,d_norm,pvec[1])
	g[3]= phase.g(Atom1_R,K,d_norm,pvec[2])
	#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))
	g_conj[0]=phase.g(Atom2_R,K,d_norm,pvec[0],'s')# 1 + np.exp(-1j*np.dot(K, Atom2_R[0])) + np.exp(-1j*np.dot(K, Atom2_R[1])) + np.exp(-1j*np.dot(K, Atom2_R[2]))
	g_conj[1]= phase.g(Atom2_R,K,d_norm,pvec[0])
	g_conj[2]= phase.g(Atom2_R,K,d_norm,pvec[1])
	g_conj[3]= phase.g(Atom2_R,K,d_norm,pvec[2])


	######################################################
	#px-py cross terms bond interactions for Exy, Exz, Eyz
	######################################################

	Epp_cross=np.linspace(0,1,6,dtype=complex)
	#Exy
	Epp_cross[0] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Exz
	Epp_cross[1] = (np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Eyz
	Epp_cross[2] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]
	#Eyx
	Epp_cross[3] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Ezx
	Epp_cross[4] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Ezy
	Epp_cross[5] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]


	#########################################################
	#Populating Hamiltonian

	Hamil=np.zeros((m,m),dtype=complex)

	#########################################################
	#######Pure states#######

	for i in range(m):
		Hamil[i,i]=orbitE_pure[i]

	#Atom2_1 coupling matrix
	coup2_1=np.zeros((P_states,In_states), dtype=complex)
	sp_conj_counter=0
	pp_counter=0

	for i in range(P_states):
		for j in range(In_states):
			if i==0 and j==0 :
				coup2_1[i,j]= g_conj[0]
			elif i==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif i==j :
				coup2_1[i,j]=Epp[i-1]*g_conj[0]
			else:
				coup2_1[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1

	#Atom1_2 coupling matrix
	coup1_2=np.zeros((In_states,P_states), dtype=complex)
	sp_counter=0
	pp_counter=0

	for i in range(In_states):
		for j in range(P_states):
			if i==0 and j==0 :
				coup1_2[i,j]= g[0]
			elif i==0 :
				coup1_2[i,j]= Esp[sp_counter] *g[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup1_2[i,j]= Esp[sp_counter] *g[j]
				sp_counter= sp_counter+1
			elif i==j :
				coup1_2[i,j]=Epp[i-1]*g[0]
			else:
				coup1_2[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1
	### Hamil final ####
	for i in range(In_states):
		for j in range(P_states):
			Hamil[i+In_states,j]=coup1_2[i,j]
			Hamil[i,j+P_states]=coup2_1[i,j]
	H=np.absolute(Hamil)

	BandE2[...,k]=np.linalg.eigvals(H)
	#BandE2[...,k]=np.linalg.eigvals(Hamil)
	#print(np.linalg.eigvals(Hamil))


for i in range(8):
	plotWidget.plot(Kpts_X,BandE2[i,...], pen=(i,8))

plotWidget.plot(Kpts_X,BandE2[0,...], pen=(8,8))



########################################################################
########################################################################
########################################################################
########################################################################


kx=np.linspace(0,0.5*np.pi/a,bandPts)
ky=np.linspace(2*np.pi/a,2*np.pi/a,bandPts)
kz=np.linspace(0,0.5*np.pi/a,bandPts)
K1=np.array([ kx , ky, kz ])
Kpts_U=np.linspace(1,1.5,bandPts)
BandE2=np.zeros((In_states+P_states,bandPts))


for k in range(bandPts):

	#################################
	#Ess and Ess_Conj
	#################################

	K=K1[...,k]

	
	g=[0,0,0,0]
	g_conj=[0,0,0,0]
	g[0]=phase.g(Atom1_R,K,d_norm,pvec[0],'s')
	g[1]= phase.g(Atom1_R,K,d_norm,pvec[0])
	g[2]= phase.g(Atom1_R,K,d_norm,pvec[1])
	g[3]= phase.g(Atom1_R,K,d_norm,pvec[2])
	#gcompare=1 + np.exp(-1j*np.dot(K, Atom1_R[0])) + np.exp(-1j*np.dot(K, Atom1_R[1])) + np.exp(-1j*np.dot(K, Atom1_R[2]))
	g_conj[0]=phase.g(Atom2_R,K,d_norm,pvec[0],'s')# 1 + np.exp(-1j*np.dot(K, Atom2_R[0])) + np.exp(-1j*np.dot(K, Atom2_R[1])) + np.exp(-1j*np.dot(K, Atom2_R[2]))
	g_conj[1]= phase.g(Atom2_R,K,d_norm,pvec[0])
	g_conj[2]= phase.g(Atom2_R,K,d_norm,pvec[1])
	g_conj[3]= phase.g(Atom2_R,K,d_norm,pvec[2])


	######################################################
	#px-py cross terms bond interactions for Exy, Exz, Eyz
	######################################################

	Epp_cross=np.linspace(0,1,6,dtype=complex)
	#Exy
	Epp_cross[0] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Exz
	Epp_cross[1] = (np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Eyz
	Epp_cross[2] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]
	#Eyx
	Epp_cross[3] = np.dot(d_norm[0],pvec[0])*np.dot(d_norm[0],pvec[1])*Vpp_sigma \
		+ np.dot((pvec[0] - d_norm[0] *np.dot(pvec[0],d_norm[0])),(pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0]) ) )*Vpp_pi \
		* g_conj[3]
	#Ezx
	Epp_cross[4] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[2]
	#Ezy
	Epp_cross[5] = (np.dot(d_norm[0],pvec[1])*np.dot(d_norm[0],pvec[2])*Vpp_sigma \
		+ np.dot((pvec[1] - d_norm[0] *np.dot(pvec[1],d_norm[0])),(pvec[2] - d_norm[0] *np.dot(pvec[2],d_norm[0]) ) )*Vpp_pi) \
		*g_conj[1]


	#########################################################
	#Populating Hamiltonian

	Hamil=np.zeros((m,m),dtype=complex)

	#########################################################
	#######Pure states#######

	for i in range(m):
		Hamil[i,i]=orbitE_pure[i]

	#Atom2_1 coupling matrix
	coup2_1=np.zeros((P_states,In_states), dtype=complex)
	sp_conj_counter=0
	pp_counter=0

	for i in range(P_states):
		for j in range(In_states):
			if i==0 and j==0 :
				coup2_1[i,j]= g_conj[0]
			elif i==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup2_1[i,j]= Esp_conj[sp_conj_counter] *g_conj[j]
				sp_conj_counter= sp_conj_counter+1
			elif i==j :
				coup2_1[i,j]=Epp[i-1]*g_conj[0]
			else:
				coup2_1[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1

	#Atom1_2 coupling matrix
	coup1_2=np.zeros((In_states,P_states), dtype=complex)
	sp_counter=0
	pp_counter=0

	for i in range(In_states):
		for j in range(P_states):
			if i==0 and j==0 :
				coup1_2[i,j]= g[0]
			elif i==0 :
				coup1_2[i,j]= Esp[sp_counter]*g[j]
				sp_conj_counter= sp_conj_counter+1
			elif j==0 :
				coup1_2[i,j]= Esp[sp_counter]*g[j]
				sp_counter= sp_counter+1
			elif i==j :
				coup1_2[i,j]=Epp[i-1]*g[0]
			else:
				coup1_2[i,j]=Epp_cross[pp_counter]
				pp_counter= pp_counter+1
	### Hamil final ####
	for i in range(In_states):
		for j in range(P_states):
			Hamil[i+In_states,j]=coup1_2[i,j]
			Hamil[i,j+P_states]=coup2_1[i,j]

	#BandE2[...,k]=np.linalg.eigvals(Hamil)#
	BandE2[...,k]=np.linalg.eigvals(np.absolute(Hamil))

	#print(np.linalg.eigvals(Hamil))


for i in range(8):
	plotWidget.plot(Kpts_U,BandE2[i,...], pen=(i,8))

plotWidget.plot(Kpts_U,BandE2[0,...], pen=(8,8))




pg.QtGui.QApplication.exec_()




