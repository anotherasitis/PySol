from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import latPoints as latpts

#creates an array of vectors between an atom and its closest neighbours,  (the bonds between such atoms)


def latvectors(polytype= 'CUBIC', latPoints=[0,0,0]):

	if polytype = 'CUBIC':
		plv= [[1,0,0],[0,1,0],[0,0,1]]

	elif polytype = 'FCC':
		plv= [[0.5,0.5,0],[0,0.5,0.5],[0.5,0,0.5]]

	elif polytype = 'BCC':
		plv= [[0.5,0.5,-0.5],[0.5,-0.5,0.5],[-0.5,0.5,0.5]]

	elif polytype = 'ZB':
		plv= [[1,0,0],[0,1,0],[0,0,1]]

	elif polytype = 'HEX':
		plv= [[1,0,0],[0,1,0],[0,0,1]]




	return latvectors