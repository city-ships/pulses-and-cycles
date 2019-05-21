
from ctypes import*
import time

import numpy as np


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
	data=c_char_p("coolllllllllllllllllllllllllllll".encode('utf-8'))
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
	data=c_char_p("coolllllllllllllllllllllllllllll".encode('utf-8'))
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
	data=c_char_p("coolllllllllllllllllllllllllllll".encode('utf-8'))
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
	phsvists=np.zeros(0)
	phdirts=np.zeros(0)
	
	print("Cancel data acquisition with Strg-C / Ctrl-C")
	
	try:
		while True:
			#time.sleep(10./1000) #pause for x ms
			# full speed is 3x realtime, not limited by printing
		
			ints,ts=pmtdata()
			#print("PMT", end = ' ')
			#print("I:",ints, end = ' ')
			#print("Ts",ts, end = ' ')
			pmtdataset=np.append(pmtdataset,int(ints))
			pmtts=np.append(pmtts,int(ts))
			
			ints,ts=phdvisdata() 
			#print("phdvis", end = ' ')
			#print("I:",ints, end = ' ')
			#print("Ts",ts, end = ' ')
			phdvisdataset=np.append(phdvisdataset,int(ints))
			phsvists=np.append(phsvists,int(ts))
			
			ints,ts=phdirdata()
			#print("phdIR", end = ' ')
			#print("I:",ints, end = ' ')
			#print("Ts",ts, end = ' ')
			#print("")
			phdirdataset=np.append(phdirdataset,int(ints))
			phdirts=np.append(phdirts,int(ts))
			
	except (KeyboardInterrupt):
		print ("Finished?")
		laseroff()
		pmtoff()
		err(mydll.rcDisconnect())
		print("Disconnecting!")
		
		print (pmtdataset)
		print(phdvisdataset)
		print (phdirdataset)
		
	
	for i in range (0,pmtdataset.size): # sanity check
		if pmtts[i]==phsvists[i]==phsirts[i]:
			continue
		else:
			print ("different timestamps!",i)
		
	
	doubles=[]
			
			
	
	for i in range (1,pmtdataset.size): # check for double entries from oversampling
		if pmtts[i-1]==phsvists[i]:
			doubles.append(i)
		else:
			continue
	
	pmtdataset=np.delete(pmtdataset,doubles) # deleting those
	phdvisdataset=np.delete(phdvisdataset,doubles)
	phdirdataset=np.delete(phdirdataset,doubles)
	pmtts=np.np.delete(pmtts,doubles)
	phsvists=np.delete(phsvists,doubles)
	phdirts=np.delete(phdirts,doubles)
	
	# writing to parent directory
	np.savetxt("../data.csv", np.transpose((pmtdataset,phdvisdataset,phdirdataset)), fmt='%.18e', delimiter='	', newline='\n', header='', footer='', comments='# ')
	
	# plotting/ file writing
	
			
			
	
	input("...Press enter to EXIT...")


		







