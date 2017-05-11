from scipy import spatial
import latPoints
import numpy as np
import itertools as itTl

class crystalStruct():

	def __init__(self, paramDict, primLatVec):
		self.atms = paramDict['atms']
		self.polyType = paramDict['Polytype']
		self.primLatVect= np.array(primLatVec)
		self.latPoints = {}
		self.latVec = {}
		self.bondVec = []
		self.startingPlane = []
		self.bounds = [1,1,1]
		self.basis = [[0,0,0]]	
		self.latpts()
		self.getLatVec()
		
	def getLatVec(self):
		Found=False
		#Uses the polytype to determine bond angles then finds nearest atom in latPoints in the direction of the bond
		if self.polyType == 'CUBIC':
			j=list(self.latPoints.keys())
			self.bondVec = np.array([[1,0,0],[0,1,0],[0,0,1]])
			for k in self.latPoints :
				for i in self.bondVec[...,]:
					found = True
					bond = i+self.latPoints[k]
					count = 0
					while not np.array_equal(self.latPoints[j[count]],bond) or count > len(j):
						count = count + 1
						if count == len(j) :
							found = False
							break
								
					if found :
						self.latVec[j[count]]= np.array([[self.latPoints[k]],[bond]])

		elif self.polyType == 'FCC':
			cubePoints=latPoints.latpts()
			#Uses the polytype to determine bond angles then finds nearest atom in latPoints in the direction of the bond
			fccPoints = latPoints.latpts(np.array([[0,0,0]]), np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]))
			j = list(fccPoints.keys())
			c = list(cubePoints.keys())
			self.bondVec = np.array([[1,0,0],[0,1,0],[0,0,1]])
			bondVec2 = np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5],[-0.5,0.5,0],[0,-0.5,0.5],[0.5,0,-0.5],[0.5,-0.5,0],[0,0.5,-0.5],[-0.5,0,0.5],[-0.5,-0.5,0],[0,-0.5,-0.5],[-0.5,0,-0.5]])
			print(cubePoints)
			for k in cubePoints:
				print(cubePoints[k])
				for i in bondVec2:
					found = True
					bond = i + cubePoints[k]
					count = 0
					while not np.array_equal(fccPoints[j[count]],bond): # or count > len(j):
						count = count + 1
						if count == len(j) :
							found = False
							break
					
					if found :
						if k in self.latVec.keys() :
							self.latVec[k]= np.append(self.latVec[k],[[bond]], axis=0)
							
						else:
							self.latVec[k]= np.array([[cubePoints[k]],[bond]])

		elif self.polyType == 'BCC':
			j=list(self.latPoints.keys())
			self.bondVec = [[0.5,0.5,-0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5]]
			for k in self.latPoints :
				for i in self.bondVec[...,]:
					found = True
					bond = i+self.latPoints[k]
					count = 0
					while not np.array_equal(self.latPoints[j[count]],bond) or count > len(j):
						count = count + 1
						if count == len(j) :
							found = False
							break
					if found :
						self.latVec[j[count]]= np.array([[self.latPoints[k]],[bond]])

		elif self.polyType == 'ZB':
			plv = np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]])
			tethe = np.array([[0.25,0.25,0.25],[0.25,-0.25,-0.25], [-0.25,0.25,-0.25],[-0.25,-0.25,0.25]])
			ZBpts = latpts.latpts(np.array([[0,0,0],[0.25,0.25,0.25]]),plv)
			self.latVec = {}
			for k in ZBpts:
				self.latVec[k] = np.array( [ ZBpts[k], ZBpts[k]+tethe[0], ZBpts[k]+tethe[1], ZBpts[k]+tethe[2], ZBpts[k]+tethe[3] ])

	def latpts(self): #, plane = false):
		for i in self.basis:
			self.latPoints[i[0]*100+i[1]*10+i[2]]=i
			for j in self.primLatVect:
			#Note bounds should be adjusted to be the solutions to being in or outside a volume (spacial testing for non rectangular shapes)
				if i[0] + j[0] <= self.bounds[0] and i[1] + j[1] <= self.bounds[1] and i[2] + j[2] <= self.bounds[2]:
					a=(i[0]*100+i[1]*10+i[2])+(j[0]*100+j[1]*10+j[2])
					self.latPoints[a] = i + j

	def calcPhononCurve(self):
		pass