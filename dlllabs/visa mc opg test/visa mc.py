
#check this for some hints:
#https://forums.ni.com/t5/Instrument-Control-GPIB-Serial/Assigning-parameters-for-write-ascii-values-in-pyvisa-for-serial/td-p/3669274?profile.language=en




import visa #pyVISA (Virtual Instrument Software Architecture)
from visa import constants
import time
rm = visa.ResourceManager()
#rm=visa.ResourceManager('@py')
test=rm.list_resources()

print (test)

#exit()

def setmcwl (wl):
	if wl>600:
		wl=600
	if wl<300:
		wl=300
	values = list(range(0))  # is needed to make this work
	Mc.write_ascii_values(str(wl)+" GOTO",values)##
	time.sleep(.5)
	#time.sleep(4) # worst case 600nm-> 300
	for i in range (1,10):
		time.sleep(500./1000)
		#resp=(Mc.query_ascii_values("MONO-?DONE\r",converter='s'))
		try:
			resp=Mc.query_ascii_values("",converter='s')
			return
		except:
			resp="Took a bit longer!"
		print (resp)
		del resp
	return
		
	
	
def readmcwl ():
	resp=Mc.query_ascii_values("?NM\r",converter='s')
	return resp[0]

print("515\sGOTO\s\sok\r\n")
print("\n\n\n")


Mc=rm.open_resource('ASRL1::INSTR', baud_rate = 9600, data_bits = 8, read_termination = '\r')

constants.VI_ASRL_STOP_ONE     
constants.VI_ASRL_PAR_NONE
constants.VI_ASRL_FLOW_NONE    

time.sleep(0.5) # time delay after initialisation












# try to set mc wavelength

lambdaopg=1000 # nanometers

lambdamc=lambdaopg/2-1  #  shg and mc finetuning

setmcwl(lambdamc)
print("Good to go")	








#Close the connection
Mc.close()
