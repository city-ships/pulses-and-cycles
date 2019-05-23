import pyqtgraph as pg
import numpy as np
app = pg.mkQApp()


view = pg.GraphicsLayoutWidget()
view.show()
w1 = view.addPlot()

class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, x, y):
        """x and y are 2D arrays of shape (Nplots, Nsamples)"""
        connect = np.ones(x.shape, dtype=bool)
        connect[:,-1] = 0 # don't draw the segment between each trace
        self.path = pg.arrayToQPath(x.flatten(), y.flatten(), connect.flatten())
        pg.QtGui.QGraphicsPathItem.__init__(self, self.path)
        self.setPen(pg.mkPen('w'))
    def shape(self): # override because QGraphicsPathItem.shape is too expensive.
        return pg.QtGui.QGraphicsItem.shape(self)
    def boundingRect(self):
        return self.path.boundingRect()

#now = pg.ptime.time()

for i in range (0,5):
	n=500

	y = np.random.normal(size=(1,n), scale=0.2) + np.arange(1)[:,np.newaxis]
	x = np.empty((1,n))
	x[:] = np.arange(n)[np.newaxis,:]
	
	lines = MultiLine(x, y)
	w1.addItem(lines)
#print ("Plot time: %0.2f sec" % (pg.ptime.time()-now))

app.exec_()
