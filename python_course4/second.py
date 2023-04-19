import time
import threading
def proc():
    print('sleeping ...')
    time.sleep(1)
    print('done')  
start = time.perf_counter()
proc()
proc()
t1 = threading.Thread(target=proc)
t2 = threading.Thread(target=proc)
t1.start()
t2.start()
t1.join()
t2.join()
stop = time.perf_counter()
print('time:',stop-start)