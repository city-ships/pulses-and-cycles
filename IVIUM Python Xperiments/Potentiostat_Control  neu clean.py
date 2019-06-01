

import numpy as np
import time
from ctypes import*
from numba import jit
# programming safety precautions



# specs are in the manual on page 295 

maxcurrent=float(0.027) # amps +/-30 mV max

def savecurrent(amps):
	if np.absolute(amps)>maxcurrent:
		print("error: current out of bounds!")
		return maxcurrent*np.sign(maxcurrent)
	else:
		return maxcurrent

maxpotential=float(3.6) # +/-4 V max # normal operation

# extendet range  up to 7.5V
@jit(cache=True)
def savepotential(volts):
	if np.absolute(volts)>maxpotential:
		print("error: potential out of bounds!")
		return maxpotential*np.sign(volts)
	else:
		return volts
@jit(cache=True)
def trivolt(u1,u2,p,t0,tt):
	u1=savepotential(u1)
	u2=savepotential(u2)
	t=tt-t0
	tau=(t%p)/p
	du=u2-u1
	voltage= u2-du*np.absolute(2*(tau-0.5))
	return round (voltage,6) # just for better loking results
	#return voltage

#0=successfully executed, -1= no device, 1=illegal command, 2=argument out of range.
def err(ret):
	errs=["OK","illegal command","argument out of range","no device"]
	print (errs[ret],ret)
				
		
#https://www.webucator.com/blog/2015/08/python-clocks-explained/
# good read for timing things


		






	

if __name__ == "__main__":
	samprate=100 # sampling rate Hz 
	scanrate=10/1000 # 2-20 mV/s range 
	dt= 1/samprate
	meastime=10
	
	u1=-1
	u2=1
	period=2*np.absolute(u2-u1)/scanrate
	
	print(period,"seconds")
	





	num=0
	
	while time.perf_counter()%1>0.001: # wait for full second
		continue
		
	
	# import  dll
	mydll = WinDLL("IVIUM_remdriver.dll")
	
	
	
	

	stat=c_int(-5555) # return variable
	one=c_int(1)
	zero=c_int(0)
	
	
	print ("Open Remdriver")
	err(mydll.IV_open())

	
	stat=mydll.IV_version()
	print("version number of the IVIUM_remdriver.dll the active IviumSoft needs",stat)
	
	serialn=c_char_p("-1".encode('utf-8'))
	
	print ("Serial Number: requesting ... ")	# if this works, the Compactstat.h is connected!
	err(mydll.IV_readSN ( serialn))
	print("Serial Number:",serialn.value.decode("ascii"), "<- number should be here")

	
	#err(mydll.IV_abort()) # little weird error
	#print("Cancelling Method")	
	

	



	print ("Trying to connect:")	
	err(mydll.IV_connect (byref(one)) ) #Connect to selected device, int=1 for connect, int=0 for disconnect
	
	#Select configuration, 0=off; 1=EStat4EL(default),
	#2=EStat2EL, 3=EstatDummy1, 4=EStatDummy2,
	#5=EstatDummy3, 6=EstatDummy4, 7=Istat4EL,
	#8=Istat2EL, 9=IstatDummy, 10=BiStat4EL, 11=BiStat2EL
	conn=c_int(0)
	print("Setting Connectionmode to",conn.value)
	err(mydll.IV_setconnectionmode (byref(conn)))
	
	
	print("Reading Potential")
	V=c_double(-333)
	err(mydll.IV_getpotential (byref(V)))
	print (V.value,"Volts")
	
	print("Reading Current")
	I=c_double(-666)
	err(mydll.IV_getcurrent (byref(I)))
	print (I.value,"Amps")	
	
	zeit=trivolt(u1,u2,period,0.,time.perf_counter()) # call to get things compiled into the cache
	t0=time.perf_counter()
	for sd in range (0,1000):
	#	if sd==1:
	#		t0=time.perf_counter()
			
		zeit=trivolt(u1,u2,period,t0,time.perf_counter())
	print(time.perf_counter()-t0,"seconds")
	

	print ("Closing Connection")	
	err(mydll.IV_connect (byref(zero)) )

	

	print("closing driver")	
	err(mydll.IV_close())

	
	
	
	
	print("\nend")
	
