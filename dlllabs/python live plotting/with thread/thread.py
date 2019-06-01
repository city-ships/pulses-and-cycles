# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time, threading
#code from
#https://gist.github.com/Overdrivr/ae1df2e08335f990f2c4

# This function is responsible for displaying the data
# it is run in its own process to liberate main process
def display(name,q):
	app2 = QtGui.QApplication([])

	win2 = pg.GraphicsWindow(title="Basic plotting examples")
	win2.resize(1000,600)
	win2.setWindowTitle('pyqtgraph example: Plotting')
	p2 = win2.addPlot(title="Updating plot")
	curve = p2.plot(pen='g') # colour

	x_np = [] # empty list?
	y_np = []
	#x_np = [1,2,3] # empty list?
	#y_np = [3,3,3]

	def updateInProc(curve,q,x,y):
		item = q.get()
		x.append(item[0])
		y.append(item[1])
		curve.setData(x[-500:] ,y[-500:] )

	timer = QtCore.QTimer()
	timer.timeout.connect(lambda: updateInProc(curve,q,x_np,y_np))
	timer.start(1) # ms to wait before plotting next point

	QtGui.QApplication.instance().exec_()


# This is function is responsible for reading some data (IO, serial port, etc)
# and forwarding it to the display
# it is run in a thread
def io(running,q):
	i = 1
	srate=50
	I=np.zeros(0)
	tt=np.zeros(0)
	t0=time.perf_counter()
	while running.is_set():
		while ((time.perf_counter()-t0)*srate<=i):
			continue
		#print (((time.perf_counter()-t0)*1000)%20)
		t=time.perf_counter()-t0
		s = np.sin(2 * np.pi * t*5)

		q.put([t,s])
		I=np.append(I,s)
		tt=np.append(tt,t)
		#time.sleep(0.02)
		i+=1
		print(t)


	
	datasave=np.transpose((I,tt))
	descr=input("Short measurement description:")
	head=descr+"\nintensity	time"
	np.savetxt("./datarrr.csv", datasave, delimiter='	', newline='\n', header=head, footer='', comments='#')
	print("Data has been saved!")

if __name__ == '__main__':
	q = Queue()
	# Event for stopping the IO thread
	run = threading.Event()
	run.set()

	# Run io function in a thread
	t = threading.Thread(target=io, args=(run,q))
	t.start()


	# Start display process
	p = Process(target=display, args=('bob',q))
	p.start()

	
	#custom code here .. 
		
	for i in range (0,10):
		#time.sleep(1)
		print("wait")

	#input("See ? Main process immediately free ! Type any key to quit.\n")
	print("Close Graph to stop and save data")

	while p.is_alive():
		time.sleep(0.33)
		pass
		
	run.clear()
	print("Waiting for scheduler thread to join...")
	t.join()
	print("Waiting for graph window process to join...")
	p.join()
	print ("Finished!")
	
	
	

	
#print("Process joined successfully. C YA !")


