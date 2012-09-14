from socket import gethostbyaddr
import ping
import nmap
import dbconnect as db
from pysnmp.entity.rfc3413.oneliner import cmdgen
import MySQLdb as mdb

commStr="public"
interfaceIp = []

def is_Managed(ip,comm_str,oid):
	snmp_version=0
	comm_data = cmdgen.CommunityData('test-agent', comm_str)
	transport = cmdgen.UdpTransportTarget((ip, 161))
	errorIndication, errorStatus,errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
		comm_data,
		transport,
		oid
		)

	if errorIndication:
		print errorIndication
	else:
		if errorStatus:
			print '%s at %s\n' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?'
				)
		else:
			snmp_version = 2
			for name, val in varBinds:
				print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
				print snmp_version
	if not snmp_version:
		comm_data = cmdgen.CommunityData('test-agent', comm_str, 0)
		errorIndication, errorStatus,errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
		comm_data,
		transport,
		oid
		)
		if errorIndication:
			print errorIndication
		else:
			if errorStatus:
				print '%s at %s\n' % (
					errorStatus.prettyPrint(),
					errorIndex and varBinds[int(errorIndex)-1] or '?'
					)
			else:
				snmp_version = 1
				for name, val in varBinds:
					print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
					print snmp_version
	return snmp_version

def is_up(ip, timeout, num_tries):
	for i in xrange(num_tries):
		result = ping.do_one(ip,timeout)
		if not result is None:
			return True
	
	# If it reached here without returning then the ping scan failed.
	# now do a tcp syn scan
	nm = nmap.PortScanner()
	res = nm.scan(hosts=ip, arguments="-n -sP -PE -PA21,23,80,3389")
	return res['scan'].values()[0]['status']['state'] == "up"
	

def dns_name(ip):
	try:
		output = gethostbyaddr(ip)
		return output[0]
	except:
		return None
	
def findLinks(ip,routetype,nexthop,rangeip,cr):
	print "called find links"
	for x in range(0,len(nexthop)):
		print x
		if routetype[x]== '4' and isInRange(nexthop[x],rangeip):
			db.db_createLink(ip,nexthop[x],cr)

def deviceType(ser,dot1dbridge):
	(l7,l4,l3,l2,l1)=(0,0,0,0,0)
	if ser>15:
		l7=1
		ser-=64
	if ser>7:
		l4=1
		ser-=8
	if ser>3:
		l3=1
		ser-=4
	if ser>1:
		l2=1
		ser-=2
	l1=ser
	if dot1dbridge!=0: b=1
	else: b=0
	if l2==1:
		if l3==1:
			if b==1: dtype="L3 switch with bridge mib"
			elif l7==1: dtype="Application switch or router"
			else: dtype="Router"
		elif b==1: dtype="L2 Switch"
		else: dtype="Host"
	elif l3==1:
		if l4==1: dtype="L4 Switch"
		elif l7==1: dtype="Application switch or router"
		else: dtype="Router"
	else: dtype="Host"
	return dtype
	
def snmp_walk(ip,commStr,oid,snmp_version):
	oid_value = []
	if snmp_version == 1:
		comm_data = cmdgen.CommunityData('test-agent', commStr, 0)
	elif snmp_version == 2:
		comm_data = cmdgen.CommunityData('test-agent',commStr)
	else:
		print "Error: not a valid version of snmp"
	transport = cmdgen.UdpTransportTarget((ip, 161))
	errorIndication, errorStatus, errorIndex,varBindTable = cmdgen.CommandGenerator().nextCmd(  
				comm_data,  #SNMP V2
				transport,
				oid  
			)
	
	if errorIndication:
	   print errorIndication
	else:
		if errorStatus:
			print '%s at %s\n' % (
				errorStatus.prettyPrint(),
				errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
				)
		else:
			for varBindTableRow in varBindTable:
				for name, val in varBindTableRow:
					oid_value.append(val.prettyPrint())
	return oid_value

def snmp_get(ip,commStr,oid,snmp_version):
	if snmp_version == 1:
		comm_data = cmdgen.CommunityData('test-agent', commStr, 0)
	elif snmp_version == 2:
		comm_data = cmdgen.CommunityData('test-agent',commStr)
	else:
		print "Error: not a valid version of snmp"
	transport = cmdgen.UdpTransportTarget((ip, 161))
	errorIndication, errorStatus, errorIndex,varBinds = cmdgen.CommandGenerator().getCmd(  
				comm_data,  
				transport,
				oid 
			)
	if errorIndication:
		print errorIndication
	else:
		if errorStatus:
			print '%s at %s\n' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?'
				)
		else:
			for name, val in varBinds:
				print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
				value_oid = val.prettyPrint()
	return value_oid	

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

def isInRange(ip,rangeip):
	flag=0
	for x in rangeip:
		if compare_ips(x[0],ip)<=0 and compare_ips(ip,x[1])<=0: flag=1
	return flag

def cleartables(dbname):
	dbase=mdb.connect("localhost","root","pass",dbname)
	cursor=dbase.cursor()
	cursor.execute("delete from ne")
	cursor.execute("delete from link")
	cursor.execute("delete from config")
	cursor.execute("delete from ip_info")
	cursor.execute("delete from phyLink")
	
def process(ip,rangeip,dbname):
	'''All the work to be done on each ip in the range'''
	dbase=mdb.connect("localhost","root","pass",dbname)
	cursor=dbase.cursor()
	timeout=2
	num_tries=2
	if db.isScanned(ip,cursor)!=1:
		if is_up(ip,timeout,num_tries):
			name=dns_name(ip)
			sys_oid = (1,3,6,1,2,1,1,1,0)
			managed=is_Managed(ip, commStr, sys_oid)
			neid=db.db_createNE('Unknown',cursor)
			db.db_createIpInfo(ip,name,managed,neid,cursor)
			if managed!=0:
				for x in range(1,8):
					oid=(1,3,6,1,2,1,1,x,0)
					a=snmp_get(ip,commStr,oid,managed)
					db.db_insert_config(neid,','.join([str(x) for x in oid]),a,cursor)
				bridge_oid=(1,3,6,1,2,1,17,1,2,0)
				bridge=snmp_get(ip,commStr,bridge_oid,managed)
				db.db_insert_config(neid,','.join([str(x) for x in bridge_oid]),bridge,cursor)

				services=db.db_getOIDconfig("1,3,6,1,2,1,1,7",neid,cursor)
				bridge=db.db_getOIDconfig("1,3,6,1,2,1,17,1,2,0",neid,cursor)
				if services is None: services=0
				if bridge is None or bridge=="": bridge=0
				netype=deviceType(int(services),int(bridge))
				db.updateNEType(neid,netype,cursor)
				
				interface_oid = (1,3,6,1,2,1,4,20,1,1)  #ipAddEnt
				ips = snmp_walk(ip,commStr,interface_oid,managed)
				for x in ips:
					if db.isScanned(x,cursor)!=1 and isInRange(x,rangeip):
						db.db_createIpInfo(x,name,managed,neid,cursor)
						name=dns_name(x)

				nexthop_oid = (1,3,6,1,2,1,4,21,1,7)
				routetype_oid = (1,3,6,1,2,1,4,21,1,8)
				nh = snmp_walk(ip, commStr, nexthop_oid, managed)				#nh=get_nextHop()
				print nh
				rt = snmp_walk(ip, commStr, routetype_oid, managed)				#rt=get_routeType()
				print rt
#				insertIntoConfig(neId,)
				findLinks(ip,rt,nh,rangeip,cursor)

def post_process(dbname):
	''' Processes the information found about the links and generates the data needed fo final topology generation'''
	dbase=mdb.connect("localhost","root","pass",dbname)
	cr=dbase.cursor()
	cr.execute("select * from link;")
	links = cr.fetchall()
	for link in links:
		dest_ne_ip = link[1]
		src_ne_id = link[0]
		# get the NE id for destination
		cr.execute('select neid from ip_info where ip="%s";'%(dest_ne_ip))
		res = cr.fetchone()
		if res is None:
			print "The ip "+dest_ne_ip+ " has not been attached to a network element yet"
			continue
		neid = res[0]
		# now store this link in the actual table.
		cr.execute('insert ignore into phyLink values (%s,%s);' % (str(src_ne_id), str(neid)))
