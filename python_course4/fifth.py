import os, threading
import time
def ping(ip):
    pingaling = os.popen("ping -n 1 "+ip,"r")
    while True:
        line = pingaling.readline()
        if not line:
            break
        if line.find('Average')>0:
            print(ip)      

start = time.perf_counter()

threads = []
for host in range(1,20):
    ip = "10.129.15."+str(host)
    # t = threading.Thread(target=ping, args=[ip])
    # t.start()
    # threads.append(t)
    ping(ip)

# for thread in threads:
#     thread.join()


stop = time.perf_counter()
print('time:',stop-start)
