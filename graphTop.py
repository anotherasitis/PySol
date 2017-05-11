###################################################################
# This project is built on pyqtgraph v 0.10.0 and so at time of 
# development, one of the key components is unfinished. As such
# (and because it's just generally good practice) great effort 
# has been made to completely isolate all the physics stuff from 
# the display stuff. Ideally, it should be feasable to completely
# replace the graphics and plotting with another library with 
# little effort. 
###################################################################

from pyqtgraph.Qt import QtCore, QtGui
import graphBase
import pyqtgraph as pg

if __name__ == '__main__':
	
	import sys
	app = pg.mkQApp()
	win = graphBase.graphBase()
	win.setWindowTitle("PySol")
	win.show()
	
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()