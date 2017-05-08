from scipy import spatial
import numpy as np
import itertools as itTl

class crystalStruct():
	def __init__(self, paramDict):
		self.atms = paramDict['atms']
		self.polyType = paramDict['Polytype']
		self.primLatVect = []
		self.latpoints = {}
		self.latVecConnect = []
		self.startingPlane = []
		self.bounds = [1,1,1]
		self.basis = [0,0,0]
		self.getPrimLatVect()
		self.latpts()

	def getPrimLatVect(self):
		pass

	def latpts(self): #, plane = false):
		pass
		# for i in self.basis[...,]:
		# 	self.latpoints[i[0]*100+i[1]*10+i[2]]=i
		# 	for j in self.primLatVect[...,]:
		# 	#Note bounds should be adjusted to be the solutions to being in or outside a volume (spacial testing for non rectangular shapes)
		# 		if i[0] + j[0] <= self.bounds[0] and i[1] + j[1] <= self.bounds[1] and i[2] + j[2] <= self.bounds[2]:
		# 			a=(i[0]*100+i[1]*10+i[2])+(j[0]*100+j[1]*10+j[2])
		# 			self.latpoints[a] = i + js

	def calcPhononCurve(self):
		pass