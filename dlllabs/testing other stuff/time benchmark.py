import time


changes=[]

changes=[]

t, num, t_orig = 0, 0, time.process_time()
for i in range(1000000):
    t = time.process_time()
changes.append( ('process_time()2', num, t - t_orig) )

t, num, t_orig = 0, 0, time.perf_counter()
for i in range(1000000):
    t = time.perf_counter()
changes.append( ('perf_counter()', num, t - t_orig) )

t, num, t_orig = 0, 0, time.monotonic()
for i in range(1000000):
    t = time.monotonic()
changes.append( ('monotonic()', num, t - t_orig) )

changes.sort(key=lambda c:c[1], reverse=True)
for i, c in enumerate(changes, 1):
    print(i, '. ', c[0], ': ', c[1], ', ', c[2], sep='')
