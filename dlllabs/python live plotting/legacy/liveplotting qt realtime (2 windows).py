# amazin code from:
#https://stackoverflow.com/questions/45046239/python-realtime-plot-using-pyqtgraph

# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
#from scipy import signal
import time

#import serial

## Create object serial port
#portName = "COM12"                      # replace this port name by yours!
#baudrate = 9600
#ser = serial.Serial(portName,baudrate)

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Signal from potomultiplier and photodiode") # creates a window
win.showMaximized()
p = win.addPlot(title="Photomuliplier")  # creates empty space for the plot in the window
curve = p.plot()                        # create an empty "plot" (a curve to plot)

windowWidth = 500                       # width of the window displaying the curve
Xm = linspace(0,0,windowWidth)          # create array that will contain the relevant time series
ptr = -windowWidth

## second windowm-> code here

p2 = win.addPlot(title="Photodiode (VIS)")  # creates empty space for the plot in the window
curve2 = p2.plot()                        # create an empty "plot" (a curve to plot)

#windowWidth = 500                       # width of the window displaying the curve
Xm2 = linspace(0,0,windowWidth)          # create array that will contain the relevant time series
ptr2 = -windowWidth


# Realtime data plot. Each time this function is called, the data display is updated

def update(value):
	size=value.size
	global curve, ptr, Xm
	Xm[:-size] = Xm[size:]                      # shift data in the temporal mean 1 sample left
	#value = ser.readline()                # read line (single value) from the serial port
	Xm[-size:] = value                 # vector containing the instantaneous values
	ptr += size                              # update x position for displaying the curve
	#Xms=0.1*Xm+sin(ptr/50) # smoothing
	curve.setData(Xm)                     # set the curve with this data
	curve.setPos(ptr,0)                   # set x position in the graph to 0
	#QtGui.QApplication.processEvents()    # you MUST process the plot now (1x reicht)
	#time.sleep (0.5)

def update2(value):
	size=value.size
	global curve2, ptr2, Xm2
	Xm2[:-size] = Xm2[size:]                      # shift data in the temporal mean 1 sample left
	#value = ser.readline()                # read line (single value) from the serial port
	Xm2[-size:] = value                 # vector containing the instantaneous values
	ptr2 += size                              # update x position for displaying the curve
	#Xms=0.1*Xm+sin(ptr/50) # smoothing
	curve2.setData(Xm2)                     # set the curve with this data
	curve2.setPos(ptr2,0)                   # set x position in the graph to 0
	QtGui.QApplication.processEvents()    # you MUST process the plot now
	#time.sleep (0.5)

### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot
for i in range(333):
	update(random.rand(3)+i/100+2*sin(i/5.))
	update2(random.rand(3)-i/100)





### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################

