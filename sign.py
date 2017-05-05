import numpy as np
#Determines the sign of a dot product for the phase term of the hamiltonian matrix elements
def sign(d,b):
	if np.dot(d,b)<= 0:
		return -1
	elif np.dot(d,b)> 0:
		return 1
	return null


