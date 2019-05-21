print("Doing some DLL Stuff!\n")

import numpy as np


# programming safety precautions





maxcurrent=float(0.1) # amps

def savecurrent(amps):
	if amps<float(0.01):
		amps=-amps
		print("error: neg amps!")
	if amps>maxcurrent:
		print("error: max amps triggered!")
		return maxcurrent
	else:
		return amps

maxpotential=float(0.5) # volts
def savepotential(volts):
	if np.absolute(volts)>maxpotential:
		print("error: potential out of bounds!")
		return maxpotential*np.sign(volts)
	else:
		return volts



			
		
#https://www.webucator.com/blog/2015/08/python-clocks-explained/
# good read for timing things


		

import time
import datetime


	
# better:https://stackoverflow.com/questions/42565297/precise-loop-timing-in-python	
# best yet has slow drift



if __name__ == "__main__":
	srate=100 # sampling rate Hz 

	


	dt= 1/srate
	seconds=10
	start=time.process_time()


	#print (time.get_clock_info("perf_counter"))
	num=0
	
	while time.perf_counter()%1>0.001:
		continue
		

	
	t0=time.perf_counter()
	times=np.zeros(0)

	for i in range (0,srate*10+1):
		#t=time.perf_counter()
		# 0.0199999 is a good number
		while ((time.perf_counter()-t0)*srate<=i):
		#while time.perf_counter()%(0.02)>0.001:
			num+=1
			continue
		times=np.append(times,time.perf_counter())
		print(i/(times[i]-t0),"Hz",end="\r")
			


	
	
	#for i in range (0,10**3):
		#time.sleep(0.00000000001)
		
	
	
	
	
		
	tend=time.perf_counter()
	delta=np.roll(times,-1)-times
	delta=np.delete(delta,-1)
	print(delta)
	print(np.mean(delta)*1000,np.std(delta)*1000)
	print (t0)
	print (tend-t0)
	print ((num)/(50*10))
	
		
	


		

	
	
	
	exit()
	
	from ctypes import*
	
	# import  dll
	mydll = WinDLL("IVIUM_remdriver.dll")
	
	
	
	
	# general return codes
	#0=successfully executed, -1= no device, 1=illegal command, 2=argument out of range.
	
	stat=mydll.IV_open()
	print("Open",stat)
	
	stat=mydll.IV_version()
	print("version number of the IVIUM_remdriver.dll the active IviumSoft needs",stat)	
	
	#stat=mydll.IV_selectdevice (2)  # needs probably device
	#print("Device Selection",stat)
	
	stat=mydll.IV_getdevicestatus
	print("Device Status",stat)
	
	IV_connect (1)  #Connect to selected device, int=1 for connect, int=0 for disconnect
	

	
	IV_connect (0)
	
	stat=mydll.IV_close()
	print("close",stat)
	
	
	
	
	print("\nend")
	
