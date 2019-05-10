import visa #pyVISA (Virtual Instrument Software Architecture)
from visa import constants
import time
rm = visa.ResourceManager()
#rm=visa.ResourceManager('@py')
test=rm.list_resources()

print (test)

def setopgwl(wl):
	if wl< 685:
		wl=685
	if wl>1063:
		wl=1063
	values = list(range(5))  # is needed to make this work
	OPG.write_ascii_values("[W0/S"+str(wl)+"]",values)
	return
	

OPG=rm.open_resource('ASRL4::INSTR', baud_rate = 38400, data_bits = 8, read_termination = '\r')

constants.VI_ASRL_STOP_ONE     
constants.VI_ASRL_PAR_NONE
constants.VI_ASRL_FLOW_NONE  

time.sleep(0.5)


setopgwl(800.39)




OPG.close()
