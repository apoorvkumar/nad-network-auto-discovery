import MySQLdb as mdb
db=None
cursor=None
def getdb():
	global db
	global cursor
	if db is None:
		db=mdb.connect("localhost","root","pass","ad")
		cursor=db.cursor()
	return cursor

#returns id of inserted ne
def db_createNE(netype, cr):
	cr.execute('INSERT INTO ne(type) values("%s")'%(netype))
	cr.execute('select max(id) from ne')
	return cr.fetchone()[0]

#return 1 if insertion succesfull, 0 if not
def db_createLink(src,dest,cr):
	cr.execute('SELECT neid from ip_info where ip="%s"'%(src))
	y=cr.fetchone()[0]
	z=cr.execute('INSERT IGNORE INTO link VALUES("%d","%s")'%(y,dest))

def db_createIpInfo(ip,name,managed,neid,cr):
	z=cr.execute('INSERT INTO ip_info(ip,name,managed,neid) VALUES("%s","%s","%d","%d")'%(ip,name,managed,neid))

def db_insert_config(neid,oid,value,cr):
	z=cr.execute('INSERT INTO config(neid,oid,value) VALUES("%d","%s","%s")'%(neid,oid,mdb.escape_string(value)))

def db_getOIDconfig(oid,neid,cr):
	z=cr.execute('SELECT value FROM config WHERE oid="%s" && neid="%d"'%(oid,neid))
	if z!=0: return cr.fetchone()[0]
	else: return None

def updateNEType(neid,netype,cr):
	cr.execute('UPDATE ne set type="%s" where id="%d"'%(netype,neid))

def isScanned(ip,cr):
	z=cr.execute('SELECT ip from ip_info WHERE ip="%s"'%(ip))
	if z!=0: return 1
	else: return 0

