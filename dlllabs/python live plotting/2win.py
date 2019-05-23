

# Import libraries
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time




### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)


win = pg.GraphicsWindow(title="Signal from potomultiplier and photodiode") # creates a window
win.showMaximized()


p = win.addPlot(title="Photomuliplier")  # creates empty space for the plot in the window
curve = p.plot()                        # create an empty "plot" (a curve to plot)
windowWidth = 500                       # width of the window displaying the curve
Xm = np.linspace(0,0,windowWidth)          # create array that will contain the relevant time series
ptr = -windowWidth

## second windowm-> code here

p2 = win.addPlot(title="Photodiode (VIS)")  # creates empty space for the plot in the window
curve2 = p2.plot()                        # create an empty "plot" (a curve to plot)
Xm2 = np.linspace(0,0,windowWidth)          # create array that will contain the relevant time series
ptr2 = -windowWidth


# Realtime data plot. Each time this function is called, the data display is updated

def update(value):
	size=value.size
	global curve, ptr, Xm
	Xm[:-size] = Xm[size:]                      # shift data in the temporal mean 1 sample left
	Xm[-size:] = value                 # vector containing the instantaneous values
	ptr += size                              # update x position for displaying the curve
	curve.setData(Xm)                     # set the curve with this data
	curve.setPos(ptr,0)                   # set x position in the graph to 0
	#QtGui.QApplication.processEvents()    # you MUST process the plot now (1x reicht)

def update2(value):
	size=value.size
	global curve2, ptr2, Xm2
	Xm2[:-size] = Xm2[size:]                      # shift data in the temporal mean 1 sample left
	Xm2[-size:] = value                 # vector containing the instantaneous values
	ptr2 += size                              # update x position for displaying the curve
	curve2.setData(Xm2)                     # set the curve with this data
	curve2.setPos(ptr2,0)                   # set x position in the graph to 0
	#QtGui.QApplication.processEvents()    # you MUST process the plot now

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot
for i in range(333):
	update(np.random.rand(3)+i/100+2*np.sin(i/5.))
	update2(np.random.rand(3)-i/100)
	#time.sleep(0.1)


win.close()

exit() # not pretty

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################

