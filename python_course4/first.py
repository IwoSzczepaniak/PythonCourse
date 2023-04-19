 # import threading

class Hello(): # class Hello(threading.Thread)
    def run(self):
        for i in range(10):
            print('hello')
class Hi(): # class Hi(threading.Thread)
     def run(self):
        for i in range(10):
            print('hi')

t1 = Hello()
t2 = Hi()

t1.run() # t1.start()
t2.run() # t2.start()

# t1.join()
# t2.join()

print('stop')
