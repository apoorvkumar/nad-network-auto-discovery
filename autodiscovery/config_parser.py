from xml.dom import minidom

#Gets the configuration from config.xml
def get_config():
	filename = "config.xml"
	config = minidom.parse(filename)
	confs = {}
	for conf in config.getElementsByTagName("config"):
		confs[conf.getAttribute("name")] = conf

	ret = {}
	# get the value for number of threads
	ret["num_threads"] = int(confs["num_threads"].getAttribute("value"))
	#parse the ip ranges now.
	range_nodes = confs["ipranges"].getElementsByTagName("range")
	ranges = [(str(rng.getAttribute("start")),str(rng.getAttribute("end"))) for rng in range_nodes]
	ret["ip_ranges"] = ranges
	
	return ret


if __name__=="__main__":
	print get_config()
