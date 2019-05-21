import time
import partymodule as pm

pm.party()



def do_something():
    print('.', end='', flush=True)
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

