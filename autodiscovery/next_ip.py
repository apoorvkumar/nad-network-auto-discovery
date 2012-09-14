def next_ip(ip):
	'''
		returns the next ip in a lexicographic ordering to the ip 
		specified.
	'''
	components = ip.split(".")
	if not len(components) == 4 :
		raise Exception("Invalid ip address provided. Number of fields is not 4")
	
	comp_numeric = [int(c) for c in components]

	index = 3
	
	while index >= 0 and comp_numeric[index] >= 254:
		comp_numeric[index] = 1
		index -= 1
		
	comp_numeric[index] += 1
	
	comp = [str(cn) for cn in comp_numeric]
	
	return ".".join(comp)

def compare_ips(ip1 , ip2):
	'''
		compares the 2 ips provided and returns an int depending on the result.
		a -ve value implies ip1 < ip2
		0 means they are equal
	'''
	components1 = ip1.split(".")
	components2 = ip2.split(".")
	if ( not len(components1) == 4 ) or ( not len(components2) == 4 ):
		raise Exception("Invalid ip address provided. Number of fields is not 4")
	
	comp_num1 = [int(c) for c in components1]
	comp_num2 = [int(c) for c in components2]

	for i in xrange(4):
		if comp_num1[i] < comp_num2[i]:
			return -1
		elif comp_num1[i] > comp_num2[i]:
			return 1
	
	return 0

def get_ip_range(ip1 , ip2):
	'''
	returns all the ips addresses in the range described by ip1 and ip2
	as a list.
	It is however recommended to get the ip addresses one at a time while
	processing since the number of elements can become pretty large in the 
	list
	'''
	if compare_ips(ip1,ip2) > 0:
		raise Exception("invalid range specified : " + ip1 + " to " + ip2)
	
	ret = [ip1]
		
	work_ip = next_ip(ip1)
	while compare_ips(work_ip,ip2) <= 0:
		ret.append(work_ip)
		work_ip = next_ip(work_ip)	
	
	return ret

if __name__=="__main__":
	'''
		test cases for the above functions
	'''
	print next_ip("192.168.2.234")
	print next_ip("192.168.2.254")
	print next_ip("192.168.254.254")

	print compare_ips("10.6.2.254","10.6.2.252")
	print compare_ips("10.6.3.254","10.6.2.252")
	print compare_ips("10.6.3.254","10.6.4.252")
	print compare_ips("10.6.3.254","10.6.3.254")
	print compare_ips("5.6.2.254","10.6.2.252")

	print get_ip_range("10.6.2.254","10.6.2.254")
	print
	print get_ip_range("10.6.1.254","10.6.2.254")
	print
	print get_ip_range("10.6.2.254","10.6.1.254")
