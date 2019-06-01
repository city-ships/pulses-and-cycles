
from ctypes import*
#import numpy as np
#import os


mydll = WinDLL("REMOTECONTROL.dll")



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
		#exit()


# plotting in the terminal (plots are sideways)

#def cmdlineplot2x(value1,maxx1,value2,maxx2,columns):
	#if maxx1==0:
		#maxx1=1
	#if maxx2==0:
		#maxx2=1

	#columns-=1
	#columns=int(columns/2)
		
	#x1=int(np.round(value1/maxx1*(columns),0))
	#x2=int(np.round(value2/maxx2*(columns),0))
	##print('@' * x1,end="")
	##print(' ' * (columns-x1),end="")
	##print('@' * x2,end="")
	##print(' ' * (columns-x2))
	
	#print('@' * x1,' ' * (columns-x1),'@' * x2,' ' * (columns-x2),sep='')
	#return


#try:
	#columns, rows = os.get_terminal_size(0)
#except OSError:
	#columns, rows = os.get_terminal_size(1)


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
	
	






		







