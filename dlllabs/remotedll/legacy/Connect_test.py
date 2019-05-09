
print("Doing some DLL Stuff!\n")


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

def err(num):
	print(errs[num],"\n")

from ctypes import*
import time
# import  dll
mydll = WinDLL("REMOTECONTROL.dll")







print("Connecting!")
err(mydll.rcConnect(0,2))

#dev1 = c_char_p
dev1=c_char_p ("mystringgggggggggggggggggggggggggggggggggggg".encode('utf-8'))


#exit()







#err(mydll.rcGetFirstDeviceName(dev2, 1024))
mydll.rcGetFirstDeviceName(dev1, 40)

printing=str(dev1.value, 'utf-8')

print (printing)

dev2=dev1

mydll.rcGetNextDeviceName(dev2, 40)

printing=str(dev2.value, 'utf-8')

print (printing)

# switch laser ON

laser=c_char_p ("SY3PL50M:32".encode('utf-8'))
State=c_char_p ("State".encode('utf-8'))
ON=c_char_p ("ON".encode('utf-8'))
OFF=c_char_p ("OFF".encode('utf-8'))
#amp=c_char_p ("13".encode('utf-8'))

err(mydll.rcSetRegFromStringA(laser, State, ON, 0))

# set amplification

Amplification=c_char_p ("Amplification".encode('utf-8'))
amppercent=c_char_p ("15".encode('utf-8'))

err(mydll.rcSetRegFromStringA(laser, Amplification, amppercent, 0))

time.sleep(10) #seconds







# switch laser OFF

err(mydll.rcSetRegFromStringA(laser, State, OFF, 0))

print("Disconnecting!")

err(mydll.rcDisconnect())

print("The End!")




