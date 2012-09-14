import config_parser
import thread_pool
import getIpConfig
import next_ip

def get_config():
	ret= config_parser.get_config()
	#read the current db name from config file
	try:
		lines = open("dbconfig").readlines()
		ret["dbname"] = lines[0].strip()
	except:
		ret["dbname"] = "ad1"

	return ret

def switch_dbs(dbname):
	file = open("dbconfig","w")
	if dbname == "ad1":
		new_name = "ad2"
	else:
		new_name = "ad1"
		
	file.write(new_name)
	

def main():
	'''
	Temporary test script for the auto discovery module.
	'''
	config = get_config()
	dbname = config['dbname']
	getIpConfig.cleartables(dbname);

	# create the thread pool and the task_queue.
	pool = thread_pool.ThreadPool(config['num_threads'])
	
	# Now add tasks to the pool for all the ips in the iprange that we have
	ip_ranges = config['ip_ranges']
	for rng in ip_ranges:
		if getIpConfig.compare_ips(rng[0],rng[1]) > 0:
			raise Exception("invalid range specified : " + rng[0] + " to " + rng[1])
		work_ip = rng[0]
		while getIpConfig.compare_ips(work_ip,rng[1]) <= 0:
			pool.add_task(getIpConfig.process,work_ip,ip_ranges,dbname)
			work_ip = next_ip.next_ip(work_ip)	

	pool.wait()
	
	getIpConfig.post_process(dbname)
	
	switch_dbs(dbname)


if __name__=="__main__":
	main()

