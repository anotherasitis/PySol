from scipy import spatial
import latPoints
import numpy as np
import itertools as itTl

class crystalStruct():

	def __init__(self, paramDict, primLatVec):
		self.atms = paramDict['atms']
		self.polyType = paramDict['Polytype']
		self.primLatVect = primLatVec
		self.primRcpLatVec = np.empty([3,3])
		self.latPoints = {}
		self.rcpLatPnts = {}
		self.latVec = {}
		self.bondVec = []
		self.startingPlane = []
		self.bounds = np.array([1,1,1])
		self.basis = []
		self.rcpScale = ''
		self.getBasis()
		self.latpts()
		self.getLatVec()
		# print(self.latVec)
		self.getRcpLatPnts()
		
	def reInitalizeAllDat(self):
		self.latpts()
		self.getLatVec()
		self.getRcpLatPnts()

	def getBasis(self):
		if self.polyType == 'ZB':
			self.basis = [[0,0,0],[0.25,0.25,0.25]]

		else:
			self.basis = [[0,0,0]]

		self.rcpBasis = [[0,0,0]]

	def getRcpLatPnts(self):
		self.rcpScale = 2*np.pi/np.dot(self.primLatVect[1], np.cross(self.primLatVect[2], self.primLatVect[0]))
		self.primRcpLatVec[0] = self.rcpScale*np.cross(self.primLatVect[1], self.primLatVect[2])
		self.primRcpLatVec[1] = self.rcpScale*np.cross(self.primLatVect[2], self.primLatVect[0])
		self.primRcpLatVec[2] = self.rcpScale*np.cross(self.primLatVect[0], self.primLatVect[1])
		print(self.primRcpLatVec)
		self.rcpLatPnts = latPoints.latpts(basis = self.rcpBasis, plv = self.primRcpLatVec, bounds = self.rcpScale*self.bounds)

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
			fccPoints = latPoints.latpts(self.basis, np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]))
			j = list(fccPoints.keys())
			c = list(cubePoints.keys())
			self.bondVec = np.array([[1,0,0],[0,1,0],[0,0,1]])
			bondVec2 = np.array([[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5],[-0.5,0.5,0],[0,-0.5,0.5],[0.5,0,-0.5],[0.5,-0.5,0],[0,0.5,-0.5],[-0.5,0,0.5],[-0.5,-0.5,0],[0,-0.5,-0.5],[-0.5,0,-0.5]])
			for k in cubePoints:
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
				for i in self.bondVec:
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
			tethe = np.array([[0.25,0.25,0.25],[0.25,-0.25,-0.25],[-0.25,0.25,-0.25],[-0.25,-0.25,0.25]])
			ZBpts = latPoints.latpts(np.array([[0,0,0],[0.25,0.25,0.25]]),plv)
			self.latVec = {}
			for k in ZBpts:
				self.latVec[k] = np.array( [ ZBpts[k], ZBpts[k]+tethe[0], ZBpts[k]+tethe[1], ZBpts[k]+tethe[2], ZBpts[k]+tethe[3] ])

	def latpts(self): #, plane = false):
		self.latPoints = latPoints.latpts(basis = self.basis,plv = self.primLatVect, bounds = self.bounds)
		# lat_temp = {}
		
		# for i in self.basis:
		# 	f=0
		# 	self.latPoints[i[0]*100+i[1]*10+i[2]]=i
		# 	lat_temp[i[0]*100+i[1]*10+i[2]]=i
		# 	while f<=3:
		# 		lat_temp=self.latPoints
		# 		for k in  list(self.latPoints):
		# 			for j in self.primLatVect:
		# 				a= ((i[0]*100+i[1]*10+i[2])+(j[0]*100+j[1]*10+j[2]) + 
		# 					(lat_temp[k][0]*100+lat_temp[k][1]*10+lat_temp[k][2]))

		# 				if (i[0] + j[0] + lat_temp[k][0]  <= self.bounds[0] and i[1] + j[1] + lat_temp[k][1] <= 
		# 					self.bounds[1] and i[2] + j[2] + lat_temp[k][2] <= self.bounds[2]) and (not (a in self.latPoints)) :
		# 					#b = i + j
		# 					self.latPoints[a] = i + j + self.latPoints[k]
		# 					f=0
		# 			f=f+1

	def calcPhononCurve(self):
		pass