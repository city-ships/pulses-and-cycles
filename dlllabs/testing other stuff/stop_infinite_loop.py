import time
import partymodule as pm





def do_something():
	pm.party()
	time.sleep(1)

try:
    while True:
        do_something()
except KeyboardInterrupt:
    pass
finally:
    for i in range(10):
        print(i)
    print('done!')

