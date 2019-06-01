

# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time, threading
import datetime

starttime=datetime.datetime.now().strftime("%Y %m %d %H_%M")


from  laserphdpmt import*


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


	def updateInProc(curve,q,x,y):
		item = q.get()
		x.append(item[0])
		y.append(item[1])
		#if (10*time.perf_counter())%1>0.8: #ad hoc optimisation
		curve.setData(x[-500:] ,y[-500:] )

	timer = QtCore.QTimer()
	timer.timeout.connect(lambda: updateInProc(curve,q,x_np,y_np))
	timer.start(1) # ms to wait before plotting next point

	QtGui.QApplication.instance().exec_()


# This is function is responsible for reading some data 
# and forwarding it to the display
# it is run in a thread also 
# saves data at the end
def io(running,q):
	i = 1
	srate=50
	
	pmtdataset=np.zeros(0)
	phdvisdataset=np.zeros(0)
	phdirdataset=np.zeros(0)
	pmtts=np.zeros(0)
	phdvists=np.zeros(0)
	phdirts=np.zeros(0)
	
	t0=time.perf_counter()
	while running.is_set():
		while ((time.perf_counter()-t0)*srate<=i):
			continue

		#ints,ts=pmtdata()
		t=time.perf_counter()-t0
		ints,ts=np.sin(2 * np.pi * t),t
		#ints2,ts2=phdvisdata()
		#ints3,ts3=phdirdata()
		


		q.put([ts,ints])
		
		pmtdataset=np.append(pmtdataset,int(ints))
		pmtts=np.append(pmtts,int(ts))
		

		#phdvisdataset=np.append(phdvisdataset,int(ints2))
		#phdvists=np.append(phdvists,int(ts2))
		

		#phdirdataset=np.append(phdirdataset,int(ints3))
		#phdirts=np.append(phdirts,int(ts3))
		

		#time.sleep(0.02)
		i+=1



	#datasave=np.transpose((pmtdataset,phdvisdataset,phdirdataset,pmtts,phdvists,phdirts))
	#np.savetxt("../data.csv", datasave.astype(int), fmt='%i', delimiter='	', newline='\n', header='', footer='', comments='# ')
	datasave=np.transpose((pmtdataset,pmtts))
	descr=input("Short measurement description:")
	head=descr+"\nintensity	time"
	
	np.savetxt("./M_DATA/datarrr"+str(starttime)+".csv", datasave, delimiter='	', newline='\n', header=head, footer='', comments='#')
	print("Data has been saved!")

if __name__ == '__main__':
	
	mydll = WinDLL("REMOTECONTROL.dll")
	#connect
	print("Connecting!")
	err(mydll.rcConnect(0,2))
	
	
	
	laseron() #self explainatory
	setpmtvoltage(567)
	pmton()
	
	# set amplification percentage
	
	setamp(23)
	
	
	
	
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


	print("Close Graph to stop and save data")

	while p.is_alive():
		time.sleep(0.33)

		
	pmtoff()
	laseroff()
	

		
	run.clear()
	print("Waiting for scheduler thread to join...")
	t.join()
	print("Waiting for graph window process to join...")
	
	err(mydll.rcDisconnect())
	print("Disconnecting laser!")
	
	p.join()
	print ("Finished!")
	
	
	

	






