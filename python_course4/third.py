import time
import threading
def proc(num):
    print(num,'sleeping ...')
    time.sleep(1)
    print(num,'done') 
start = time.perf_counter()
threads = []
for n in range(10):
    t = threading.Thread(target=proc, args=[n])
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()
stop = time.perf_counter()
print('time:',stop-start)