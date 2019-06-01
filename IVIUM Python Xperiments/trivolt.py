
import numpy as np

def trivolt(u1,u2,p,t0,tt):
	t=tt-t0
	tau=(t%p)/p
	du=u2-u1
	voltage= u2-du*np.absolute(2*(tau-0.5))
	return round (voltage,3) # just for better loking results
	#return voltage

	

		
		
for i in range(0,101):
	u1,u2,p,t0,tt=np.random.random(5)
	aa=trivolt(u1,u2,p,t0,tt)
	print (aa)
	#print (trivolt(0.,1.,10.,0.,i),i)
