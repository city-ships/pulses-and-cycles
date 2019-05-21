import numpy as np
import matplotlib.pyplot as plt

#plt.axis([0, 10, 0, 1])

x=[]
y=[]

for i in range(500):
    y.append(np.random.random())
    x.append(i)
    plt.plot(x[-10:], y[-10:])
    
    plt.draw()
    plt.pause(0.001)
    plt.cla()
    
    
print("nice plots")


