import numpy as np
import sign as s

def g(R,K,d,b,pOrbital= 'p') :
	
	#calculates  phase term for the LCAO bandstructure hamiltonian
	#requires:
	#R= translation vectors for neighboring atoms
	#K= momentum wavevector kx,ky,kz
	#d=unit nearest neighbor vectors
	#orbital bond vector (only pass in a single direction)
	
	if pOrbital=='p':
		g = (1 + s.sign(d[1],b)*np.exp(1j*np.dot(K,R[0])) + s.sign(d[2],b)*np.exp(1j*np.dot(K,R[1])) + s.sign(d[3],b)*np.exp(1j*np.dot(K,R[2])))
	elif pOrbital =='s':
		g = (1 + np.exp(1j*np.dot(K,R[0])) + np.exp(1j*np.dot(K,R[1])) + np.exp(1j*np.dot(K,R[2])))
	
	return g