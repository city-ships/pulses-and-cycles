
import numpy as np


import os
import sys
import time


os.system('mode con: cols=230 lines=40')

time.sleep(2)

try:
    columns, rows = os.get_terminal_size(0)
except OSError:
    columns, rows = os.get_terminal_size(1)
print (columns)

def cmdlineplot(value,maxx,columns):
	if value<0:
		value=0
	if value>maxx:
		value=maxx
	columns-=1	
	x=int(round(value/maxx*(columns),0))
	print('█' * x,end="")
	print()

	#print('.' * (columns-x))



#@jit # is slower actually
def cmdlineplot2x(value1,maxx1,value2,maxx2,columns):
	columns-=1
	columns=int(columns/2)
	
	
	
	#x1=int(round(value1/maxx1*(columns)/2,0))
	#x2=int(round(value2/maxx2*(columns)/2,0))
	
	
	x1=int(round(value1/maxx1*(columns),0))
	x2=int(round(value2/maxx2*(columns),0))
	#print('@' * x1,end="")
	#print(' ' * (columns-x1),end="")
	#print('@' * x2,end="")
	#print(' ' * (columns-x2))
	
	print('@' * x1,' ' * (columns-x1),'@' * x2,' ' * (columns-x2),sep='')
	return
	#print(,end="")
	#print('@' * x2,end="")
	#print(' ' * (columns-x2))
	#'█'
	#'█'


t0=time.perf_counter()
for i in range(0,1000):
	#cmdlineplot(1+np.sin(i/10),2,columns)
	cmdlineplot2x(1+np.sin(i/10),2,1+np.cos(i/5),2,columns)
	
print(time.perf_counter()-t0)
