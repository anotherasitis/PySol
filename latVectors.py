from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import latPoints as latpts

#creates an array of vectors between an atom and its closest neighbours,  (the bonds between such atoms)


def latVec(polytype= 'CUBIC'):
	latVec ={}
	Found=False


	#Uses the polytype to determine bond angles then finds nearest atom in latPoints in the direction of the bond
	if polytype == 'CUBIC':

		j=list(latPoints.keys())


		bondVec = np.array([[1,0,0],[0,1,0],[0,0,1]])

		for k in latPoints :
			for i in bondVec[...,]:

				found = True
				bond = i+latPoints[k]
				count = 0

				while not np.array_equal(latPoints[j[count]],bond) or count > len(j):
					count = count + 1
					if count == len(j) :
						found = False
						break
							
				if found :
					latVec[j[count]]= np.array([[latPoints[k]],[bond]])


	elif polytype == 'FCC':

		cubePoints=latPoints.latpts()
		latVec={}

			#Uses the polytype to determine bond angles then finds nearest atom in latPoints in the direction of the bond
		fccPoints = latPoints.latpts(np.array([[0,0,0]]), np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]))
		j = list(fccPoints.keys())
		c = list(cubePoints.keys())

		bondVec = np.array([[1,0,0],[0,1,0],[0,0,1]])
		bondVec2 = np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5],[-0.5,0.5,0],[0,-0.5,0.5],[0.5,0,-0.5],[0.5,-0.5,0],[0,0.5,-0.5],[-0.5,0,0.5],[-0.5,-0.5,0],[0,-0.5,-0.5],[-0.5,0,-0.5]])


		for k in cubePoints :

			for i in bondVec2[...,]:
				print(i)

				found = True
				bond = i + cubePoints[k]
				count = 0
				print(bond)

				while not np.array_equal(fccPoints[j[count]],bond): # or count > len(j):
					count = count + 1
					if count == len(j) :
						found = False
						break
				
				if found :
					if k in latVec.keys() :
						#print(latVec)
						#print([bond])
						#cubic keys over fcc keys?

						latVec[k]= np.append(latVec[k],[[bond]], axis=0)
						
					else:
						latVec[k]= np.array([[cubePoints[k]],[bond]])

	elif polytype == 'BCC':
		j=list(latPoints.keys())
		bondVec = [[0.5,0.5,-0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5]]
		for k in latPoints :
			for i in bondVec[...,]:

				found = True
				bond = i+latPoints[k]
				count = 0

				while not np.array_equal(latPoints[j[count]],bond) or count > len(j):
					count = count + 1
					if count == len(j) :
						found = False
						break

					
							
				if found :
					latVec[j[count]]= np.array([[latPoints[k]],[bond]])

	elif polytype == 'ZB':


		plv = np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]])
		tethe = np.array([ [0.25,0.25,0.25],[0.25,-0.25,-0.25], [-0.25,0.25,-0.25],[-0.25,-0.25,0.25] ])

		ZBpts = latpts.latpts(np.array([[0,0,0],[0.25,0.25,0.25]]),plv)
		latVec = {}

		for k in ZBpts:
			latVec[k] = np.array( [ ZBpts[k], ZBpts[k]+tethe[0], ZBpts[k]+tethe[1], ZBpts[k]+tethe[2], ZBpts[k]+tethe[3] ])


	return latVec



