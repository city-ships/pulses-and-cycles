
from ctypes import*
import time
import numpy as np
import os



###### PLOTTING #############

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg




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
	QtGui.QApplication.processEvents()    # you MUST process the plot now


##########################



def err(num):
	
	errs=["0K;-)",
	"RMTCTRLERR_NOMOREDATA        1  // End of registers list or enumerated values list",
	 "RMTCTRLERR_NOCFGFILE         2  // No config file found",
	 "RMTCTRLERR_WRONGCFGFILE      3  // wrong CFG file",
	 "RMTCTRLERR_BUFFERTOOSHORT    4  // application provided return buffer is too short",
	 "RMTCTRLERR_NOSUCHDEVICE      5  // no such device name",
	 "RMTCTRLERR_NOSUCHREGISTER    6  // no such register name",
	 "RMTCTRLERR_CANTCONNECT       7",
	 "RMTCTRLERR_TIMEOUT           8  // timeout waiting for device answer",
	 "RMTCTRLERR_READONLY          9  // register is read only",
	 "RMTCTRLERR_NOT_NV           10  // register is not NV",
	 "RMTCTRLERR_HILIMIT          11  // attempt to set value above upper limit",
	 "RMTCTRLERR_LOLIMIT          12  // attempt to set value below bottom limit",
	 "RMTCTRLERR_NOSUCHVALUE      13  // attempt to set not allowed value",
	 "RMTCTRLERR_NOTLOGGED        14  // register is not being logged",
	 "RMTCTRLERR_MEMORYFULL       15  // not enough memory",
	 "RMTCTRLERR_LOGISEMPTY       16  // no data in the queue yet",
	 "RMTCTRLERR_ALREADYCONNECTED 17  // already connected, please disconnect first",
	 "RMTCTRLERR_NOTYETCONNECTED  18  // not connected, please connect first"]
	if num!=0:
		print(errs[num],"\n")

# plotting in the terminal (plots are sideways)

def cmdlineplot2x(value1,maxx1,value2,maxx2,columns):

	columns-=1
	columns=int(columns/2)
		
	x1=int(np.round(value1/maxx1*(columns),0))
	x2=int(np.round(value2/maxx2*(columns),0))
	#print('@' * x1,end="")
	#print(' ' * (columns-x1),end="")
	#print('@' * x2,end="")
	#print(' ' * (columns-x2))
	
	print('@' * x1,' ' * (columns-x1),'@' * x2,' ' * (columns-x2),sep='')
	return


try:
    columns, rows = os.get_terminal_size(0)
except OSError:
    columns, rows = os.get_terminal_size(1)


#laser --------------------

def laseron():
	laser=c_char_p ("SY3PL50M:32".encode('utf-8'))
	State=c_char_p ("State".encode('utf-8'))
	ON=c_char_p ("ON".encode('utf-8'))
	print("Turning laser on!\n Status:")
	err(mydll.rcSetRegFromStringA(laser, State, ON, 0))
	# 0 means to complain if parameter ranges are incorrect
	return
	
def laseroff():
	laser=c_char_p ("SY3PL50M:32".encode('utf-8'))
	State=c_char_p ("State".encode('utf-8'))
	OFF=c_char_p ("OFF".encode('utf-8'))
	print("Turning laser off!\n Status:")
	err(mydll.rcSetRegFromStringA(laser, State, OFF, 0))
	# 0 means to complain if parameter ranges are incorrect
	return

def setamp(percent):
	if percent>70:
		percent=70
	if percent<1:
		percent=1
	laser=c_char_p ("SY3PL50M:32".encode('utf-8'))
	Amplification=c_char_p ("Amplification".encode('utf-8'))
	amppercent=c_char_p (str(int(percent)).encode('utf-8'))
	print("Setting amplification to ",percent," %")
	print("Status:")
	err(mydll.rcSetRegFromStringA(laser, Amplification, amppercent, 0))
	# 0 means to complain if parameter ranges are incorrect
	return

#photomultipliers --------------------
	
def setpmtvoltage(volts):
	if volts<0:
		volts=0
	if volts>1050:
		volts=1050
	cvolts=c_double(volts)
	PMT1=c_char_p ("PMTC0000:1".encode('utf-8'))
	command=c_char_p ("Set PMT cathode voltage".encode('utf-8'))
	err(mydll.rcSetRegFromDouble(PMT1, command, cvolts))
	return


def pmton():
	on=c_double(1)
	PMT1=c_char_p ("PMTC0000:1".encode('utf-8'))
	command=c_char_p ("PMT HV power supply".encode('utf-8'))
	err(mydll.rcSetRegFromDouble(PMT1, command, on))
	return
	
def pmtoff():
	off=c_double(0)
	PMT1=c_char_p ("PMTC0000:1".encode('utf-8'))
	command=c_char_p ("PMT HV power supply".encode('utf-8'))
	err(mydll.rcSetRegFromDouble(PMT1, command, off))
	return


# data aquisition from phdvis --------------------
	
def phdvisdata(): # seems to work, but not the timestamp
	
	phdvis=c_char_p ("PHD1K000:3".encode('utf-8'))
	datareg=c_char_p ("Data".encode('utf-8'))
	data=c_char_p("-1".encode('utf-8'))
	maxvallen=c_int(10) # max string length
	timeout=c_int(200) # milliseconds
	timestamp=c_int(-5) # writing timestamp here

	err(mydll.rcGetRegAsString(phdvis,datareg, data, maxvallen, timeout,byref(timestamp)))
	#print("phdvis", end = ' ')
	#print("I:",data.value.decode("ascii"), end = ' ')
	#print("Ts",timestamp.value, end = ' ')
	return data.value.decode("ascii"),timestamp.value
	
# data aquisition from phdvis --------------------

def phdirdata(): # seems to work, but not the timestamp
	
	phdvis=c_char_p ("PHD1K000:5".encode('utf-8'))
	datareg=c_char_p ("Data".encode('utf-8'))
	data=c_char_p("-1".encode('utf-8'))
	maxvallen=c_int(10) # max string length
	timeout=c_int(200) # milliseconds
	timestamp=c_int(-5) # writing timestamp here

	err(mydll.rcGetRegAsString(phdvis,datareg, data, maxvallen, timeout,byref(timestamp)))
	#print("phdIR", end = ' ')
	#print("I:",data.value.decode("ascii"), end = ' ')
	#print("Ts",timestamp.value, end = '')
	return data.value.decode("ascii"),timestamp.value

# data aquisition from lower PMT --------------------

def pmtdata(): # seems to work, but not the timestamp
	
	phdvis=c_char_p ("PMTC0000:1".encode('utf-8'))
	datareg=c_char_p ("Data".encode('utf-8'))
	data=c_char_p("-1".encode('utf-8'))
	maxvallen=c_int(10) # max string length
	timeout=c_int(200) # milliseconds
	timestamp=c_int(-5) # writing timestamp here

	err(mydll.rcGetRegAsString(phdvis,datareg, data, maxvallen, timeout,byref(timestamp)))
	#print("PMT", end = ' ')
	#print("I:",data.value.decode("ascii"), end = ' ')
	#print("Ts",timestamp.value, end = ' ')
	return data.value.decode("ascii"),timestamp.value
	
	


if __name__ == '__main__':
	mydll = WinDLL("REMOTECONTROL.dll")
	#connect
	print("Connecting!")
	err(mydll.rcConnect(0,2))
	
	
	
	laseron() #self explainatory
	setpmtvoltage(567)
	pmton()
	
	# set amplification percentage
	
	setamp(70)
	


	s=60
	
	pmtdataset=np.zeros(0)
	phdvisdataset=np.zeros(0)
	phdirdataset=np.zeros(0)
	pmtts=np.zeros(0)
	phdvists=np.zeros(0)
	phdirts=np.zeros(0)
	
	print("Cancel data acquisition with Strg-C / Ctrl-C")
	
	#timer =QtCore.QTimer()
	#timer.timeout.connect(lambda: None)
	#timer.start(100)
	
	
	
	i=0 # loop counter
	n=1 # points plotted at once -> faster
	times=np.zeros(0)
	while time.perf_counter()%1>0.001:	# waiting for the begin of the next second
		continue
		
	t0=time.perf_counter()
	while True:
		#time.sleep(10./1000) #pause for x ms
		# full speed is 3x realtime, not limited by printing
	
		#ints,ts=pmtdata()
		ints,ts=10*np.cos(i/10),time.perf_counter()*1000
		#print("PMT", end = ' ')
		#print("I:",ints, end = ' ')
		#print("Ts",ts, end = ' ')
		pmtdataset=np.append(pmtdataset,int(ints))
		pmtts=np.append(pmtts,int(ts))
		
		#ints,ts=phdvisdata() 
		#print("phdvis", end = ' ')
		#print("I:",ints, end = ' ')
		#print("Ts",ts, end = ' ')
		phdvisdataset=np.append(phdvisdataset,int(ints))
		phdvists=np.append(phdvists,int(ts))
		
		#ints,ts=phdirdata()
		#print("phdIR", end = ' ')
		#print("I:",ints, end = ' ')
		#print("Ts",ts, end = ' ')
		#print("")
		phdirdataset=np.append(phdirdataset,int(ints))
		phdirts=np.append(phdirts,int(ts))
		if i%n==0: # drawing plot
			pass
			#update(pmtdataset[-n:])
			#print(pmtdataset[-n:])
			#update2(phdvisdataset[-n:])
			
			#or
			maxpmt=int(np.amax(pmtdataset))
			maxphdvis=int(np.amax(phdvisdataset))
			cmdlineplot2x(np.mean(pmtdataset[-n:]),maxpmt,np.mean(phdvisdataset[-n:]),maxphdvis,columns)
			
			
		
		
		print(i/(time.perf_counter()-t0),"Hz",end="\r")

		
		
		if win.isHidden()==True: # break the loop by closing the window
			break
		i+=1





	
	print ("Finished?")
	laseroff()
	pmtoff()
	err(mydll.rcDisconnect())
	print("Disconnecting!")
	
	
	## making all datasets of equal length
	#if min(pmtdataset.size,phdirts.size)!=max(pmtdataset.size,phdirts.size):
		#minn=min(pmtdataset.size,phdirts.size)
		#pmtdataset=pmtdataset[:minn]
		#phdvisdataset=phdvisdataset[:minn]
		#phdirdataset=phdirdataset[:minn]
		
		#pmtts=pmtts[:minn]
		#phdvists=phdvists[:minn]
		#phdirts=phdirts[:minn]
		
		
		

	
	print (pmtdataset)
	print(phdvisdataset)
	print (phdirdataset)
		
	
	for i in range (0,pmtdataset.size): # sanity check
		if pmtts[i]==phdvists[i]==phdirts[i]:
			continue
		else:
			print ("different timestamps!",i)
		
	
	doubles=[]
			
	print ("Test")
	
	for i in range (1,pmtdataset.size): # check for double entries from oversampling
		if pmtts[i-1]==phdvists[i]:
			doubles.append(i)
		else:
			continue
	
	pmtdataset=np.delete(pmtdataset,doubles) # deleting those
	phdvisdataset=np.delete(phdvisdataset,doubles)
	phdirdataset=np.delete(phdirdataset,doubles)
	pmtts=np.delete(pmtts,doubles)
	phdvists=np.delete(phdvists,doubles)
	phdirts=np.delete(phdirts,doubles)
	
	# writing to parent directory
	np.savetxt("../data.csv", np.transpose((pmtdataset,phdvisdataset,phdirdataset)), fmt='%.18e', delimiter='	', newline='\n', header='', footer='', comments='# ')
	
	# plotting/ file writing
	
			
	print ("Test2")
	exit()
	### END QtApp ####
	pg.QtGui.QApplication.exec_() # you MUST put this at the end
	##################	
	
	input("...Press enter to EXIT...")



		







