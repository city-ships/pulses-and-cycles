
#check this for some hints:
#https://forums.ni.com/t5/Instrument-Control-GPIB-Serial/Assigning-parameters-for-write-ascii-values-in-pyvisa-for-serial/td-p/3669274?profile.language=en




import visa #pyVISA (Virtual Instrument Software Architecture)

rm = visa.ResourceManager() 
#rm=visa.ResourceManager('@py')
test=rm.list_resources()

print (test)

#exit()

def connect():
	print ("Connecting!")
	
def close():
	print ("Closing connection!")



Mc=rm.open_resource("COM1")




#('ASRL1::INSTR',

#OPG=rm.open_resource("COM4")

idd=Mc.query("SERIAL\r") # check if its ther and ID
model=Mc.query("MODEL\r")
wlnow=Mc.query("?NM/MIN\r") # not working

print(idd,model,wlnow)

# attemting to read from mc

#values = Mc.read_bytes(1) # dont know the register?
#print (values)

# try to set mc wavelength

lambda0=900*10**-9 # nanometers

lambdamc=lambda0/2-1  #  shg and mc finetuning

sentence="coooooooooooooooooooooooooooooooooool>"

#Mc.write_binary_values("500 GOTO\r",sentence)





#Close the connection
Mc.close()
