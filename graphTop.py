import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import graphBase

if __name__ == '__main__':
	import sys
	
	app = pg.mkQApp()
	win = graphBase.graphBase()
	win.setWindowTitle("PySol")
	win.show()
	
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()