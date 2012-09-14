import threading
import Queue

# The method used here for creating thread pools is a very common idiom used in python.
# examples of this method are available all over the internet. This implementation is inspired
# from the one that we found on stackoverflow.com

class Worker(threading.Thread):
	'''
	Class implementing a worker thread.
	The queue passed contains jobs in the form of function references along
	with the corresponding arguments that are to be passed to them
	'''
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue = queue
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kwargs = self.queue.get()
			try:
				func(*args, **kwargs)
			except Exception, e :
				print e
			finally:
				self.queue.task_done()

class ThreadPool:
	'''
	Implements a threadpool with the flexibility of adding tasks as and
	when the thread pool is needed. Also has a wait method that allows 
	waiting for jobs to finish
	'''
	def __init__(self,num_threads):
		self.tasks = Queue.Queue()
		for i in range(num_threads):
			Worker(self.tasks)
	
	def add_task(self, func, *args, **kwargs):
		self.tasks.put((func,args,kwargs))
		
	def wait(self):
		self.tasks.join()

def main():
	'''
	Test method for the thread pool.
	'''

	from random import randrange
	from time import sleep
	
	delays = [randrange(1,5) for i in range(50)]
	
	def wd(i,d):
		print str(i) + " : sleeping for " + str(d) + " seconds "
		sleep(d)
	
	pool = ThreadPool(25)
	
	for i,d in enumerate(delays):
		pool.add_task(wait_delay,i,d)
		
	pool.wait()
	
	print " All threads have joined"
	
	for i,d in enumerate(delays):
		pool.add_task(wait_delay,i,d)
		
	pool.wait()


if __name__ == "__main__":
	main()
