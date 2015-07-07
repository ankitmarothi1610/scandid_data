import MySQLdb as mdb
db = mdb.connect('localhost','admin','scandid321','scandid')
c = db.cursor()
map = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
days = [31,28,31,30,31,30,31,31,30,31,30,31]
def unregall(m,n,o,p,s): #Unregistered Users - All Platforms
	u = int(n)
	v = int(p)
	if(u==v):
		q = "SELECT COUNT(DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26)) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT COUNT(DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26)) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)	
	c.execute(q)
	res = c.fetchall()
	for row in res:
		a = row[0]
	return a
def regall(m,n,o,p,s): #Registered Users - All Platforms
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	a = []
	b = []
	i = []
	res = c.fetchall()
	for row in res:
		a.append(row[0])
		b.append(row[1])
		i.append(0)
		flag = flag + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	resu = c.fetchall()
	count = 0
	for r in resu:
		p = r[0]
		j = 0
		while(j<flag):
			if(p==a[j]):
				if(i[j]==0):
					count = count + 1
					i[j] = 1
					t = b[j]
					y = j - 1
					if(y>=0):
						while(b[y]==t):
							i[y] = 1
							y = y - 1
							if(y<0):
								break
					z = j + 1
					if(z<flag):
						while(b[z]==t):
							i[z] = 1
							z = z + 1
							if(z>=flag):
								break
				break
			j = j + 1
	return count
def unregmxfo(m,n,o,p,s,x): #Unregistered Users - Micromax/First Offer
	u = int(n)
	v = int(p)
	if(u==v):
		q = "SELECT COUNT(DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26)) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),x,s)
	else:
		q = "SELECT COUNT(DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26)) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],x,s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],x,s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),x,s)	
	c.execute(q)
	res = c.fetchall()
	for row in res:
		a = row[0]
	return a
def regmxfo(m,n,o,p,s,x): #Registered Users - Micromax/First Offer
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	a = []
	b = []
	i = []
	res = c.fetchall()
	for row in res:
		a.append(row[0])
		b.append(row[1])
		i.append(0)
		flag = flag + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s'" %(s,map[u-1],int(m),int(o),x,s,map[u-1],int(m),int(o),x)
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' " %(s,map[u-1],int(m),days[u-1],x,s,map[u-1],int(m),days[u-1],x)
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' "%(map[u-1],1,days[u-1],x,s,map[u-1],1,days[u-1],x)
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s'"%(map[u-1],1,int(o),x,s,map[u-1],1,int(o),x)
	c.execute(q1)
	resu = c.fetchall()
	count = 0
	for r in resu:
		p = r[0]
		j = 0
		while(j<flag):
			if(p==a[j]):
				if(i[j]==0):
					count = count + 1
					i[j] = 1
					t = b[j]
					y = j - 1
					if(y>=0):
						while(b[y]==t):
							i[y] = 1
							y = y - 1
							if(y<0):
								break
					z = j + 1
					if(z<flag):
						while(b[z]==t):
							i[z] = 1
							z = z + 1
							if(z>=flag):
								break
				break
			j = j + 1
	return count
def unregweb(m,n,o,p,s): #Unregistered Users - Scandid Web
	u = int(n)
	v = int(p)
	a = []
	if(u==v):
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)	
	c.execute(q)
	res = c.fetchall()
	flag = 0 #flag is the count of distinct users of scandidweb having non-empty PID
	for r in res:
		a.append(r[0])
		flag = flag + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)
	c.execute(q1)
	res = c.fetchall()
	ans = 0 #ans is the count of distinct users of scandidweb having empty PID and not in flag
	for r in res:
		b = r[0]
		counter = 0
		while(counter<flag):
			if(b==a[counter]):
				break
			counter = counter + 1
		if(counter==flag):
			ans = ans + 1
	return (ans+flag)
def unregmob(m,n,o,p,s): #Unregistered Users - Mobile Web Browser
	u = int(n)
	v = int(p)
	a = []
	if(u==v):
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)	
	c.execute(q)
	res = c.fetchall()
	flag = 0 #flag is the count of distinct users of scandidmobilesite having non-empty PID
	for r in res:
		a.append(r[0])
		flag = flag + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)
	c.execute(q1)
	res = c.fetchall()
	ans = 0 #ans is the count of distinct users of scandidmobilesite having empty PID and not in flag
	for r in res:
		b = r[0]
		counter = 0
		while(counter<flag):
			if(b==a[counter]):
				break
			counter = counter + 1
		if(counter==flag):
			ans = ans + 1
	return (ans+flag)
def unregapp(m,n,o,p,s): #Unregistered Users - Mobile App
	u = int(n)
	v = int(p)
	a = []
	if(u==v):
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)	
	c.execute(q)
	res = c.fetchall()
	flag = 0 #flag is the count of distinct users of mobile having non-empty PID
	for r in res:
		a.append(r[0])
		flag = flag + 1
	return flag
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')" %(s,map[u-1],int(m),int(o),s)
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%')"%(map[u-1],1,int(o),s)
	c.execute(q1)
	res = c.fetchall()
	ans = 0 #ans is the count of distinct users of mobile having empty PID and not in flag
	for r in res:
		b = r[0]
		counter = 0
		while(counter<flag):
			if(b==a[counter]):
				break
			counter = counter + 1
		if(counter==flag):
			ans = ans + 1
	return (ans+flag)
def regweb(m,n,o,p,s): #Registered Users - Scandid Web
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	a = []
	b = []
	i = []
	y = []
	res = c.fetchall()
	for row in res:
		a.append(row[0])
		b.append(row[1])
		i.append(0)
		flag = flag + 1 #flag is the count of total different Provisional Id's
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	resu = c.fetchall()
	f = 0
	for r in resu:
		y.append(r[0])
		f = f + 1 #f is the count of distinct Provisional Id's having non-empty mode
	u = int(n)
	v = int(p)
	if(u==v):
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q2)
	resu = c.fetchall()
	ans = 0 #ans is the count of distinct Provisional Id's having empty mode
	for r in resu:
		w = r[0]
		counter = 0
		while(counter<f):
			if(w==y[counter]):
				break
			counter = counter + 1
		if(counter==f):
			y.append(w)
			ans = ans + 1
	count = 0
	r = 0
	while(r<(f+ans)):
		p = y[r]
		j = 0
		while(j<flag):
			if(p==a[j]):
				if(i[j]==0):
					count = count + 1
					i[j] = 1
					yy = j - 1
					if(yy>=0):
						while(b[yy]==b[j]):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					z = j + 1
					if(z<flag):
						while(b[z]==b[j]):
							i[z] = 1
							z = z + 1
							if(z>=flag):
								break
				break
			j = j + 1
		r = r + 1
	return count
def regmob(m,n,o,p,s): #Registered Users - Mobile Web Browser	
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	a = []
	b = []
	i = []
	y = []
	res = c.fetchall()
	for row in res:
		a.append(row[0])
		b.append(row[1])
		i.append(0)
		flag = flag + 1 #flag is the count of total different Provisional Id's
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	resu = c.fetchall()
	f = 0
	for r in resu:
		y.append(r[0])
		f = f + 1 #f is the count of distinct Provisional Id's having non-empty mode
	u = int(n)
	v = int(p)
	if(u==v):
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q2)
	resu = c.fetchall()
	ans = 0 #ans is the count of distinct Provisional Id's having empty mode
	for r in resu:
		w = r[0]
		counter = 0
		while(counter<f):
			if(w==y[counter]):
				break
			counter = counter + 1
		if(counter==f):
			y.append(w)
			ans = ans + 1
	count = 0
	r = 0
	while(r<(f+ans)):
		p = y[r]
		j = 0
		while(j<flag):
			if(p==a[j]):
				if(i[j]==0):
					count = count + 1
					i[j] = 1
					yy = j - 1
					if(yy>=0):
						while(b[yy]==b[j]):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					z = j + 1
					if(z<flag):
						while(b[z]==b[j]):
							i[z] = 1
							z = z + 1
							if(z>=flag):
								break
				break
			j = j + 1
		r = r + 1
	return count
def regapp(m,n,o,p,s): #Registered Users - Mobile App
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	a = []
	b = []
	i = []
	y = []
	res = c.fetchall()
	for row in res:
		a.append(row[0])
		b.append(row[1])
		i.append(0)
		flag = flag + 1 #flag is the count of total different Provisional Id's
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	resu = c.fetchall()
	f = 0
	for r in resu:
		y.append(r[0])
		f = f + 1 #f is the count of distinct Provisional Id's having non-empty mode
	u = int(n)
	v = int(p)
	if(u==v):
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile'" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q2 = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q2 = q2 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile'"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q2)
	resu = c.fetchall()
	ans = 0 #ans is the count of distinct Provisional Id's having empty mode
	for r in resu:
		w = r[0]
		counter = 0
		while(counter<f):
			if(w==y[counter]):
				break
			counter = counter + 1
		if(counter==f):
			y.append(w)
			ans = ans + 1
	count = 0
	r = 0
	while(r<(f+ans)):
		p = y[r]
		j = 0
		while(j<flag):
			if(p==a[j]):
				if(i[j]==0):
					count = count + 1
					i[j] = 1
					yy = j - 1
					if(yy>=0):
						while(b[yy]==b[j]):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					z = j + 1
					if(z<flag):
						while(b[z]==b[j]):
							i[z] = 1
							z = z + 1
							if(z>=flag):
								break
				break
			j = j + 1
		r = r + 1
	return count
def showtable(): #Show Tables
	q1 = "SHOW TABLES"
	c.execute(q1)
	res = c.fetchall()
	print "The database 'scandid' has the following tables:\n"
	for r in res:
		a = r[0]
		print "%s"%(a)
showtable()
s = raw_input("\nEnter the name of the table.\n")
check = 1
while(check==1):
	t = int(raw_input("\n1 - Registered Users\n2 - Unregistered Users\n3 - All Users\n0 - Exit\n"))
	if(t==0): #Exit the program
		check = 2
		break
	elif(t==1): #Registered Users
		i = int(raw_input("\n1 - All Platforms\n2 - Scandid Web\n3 - Mobile App\n4 - Mobile Web Browser\n5 - First Offer\n6 - Micromax\n"))
		m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
		o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
		print ""
		if(i==1):
			print "%d"%(regall(m,n,o,p,s))
		elif(i==5):
			print "%d"%(regmxfo(m,n,o,p,s,'fo'))
		elif(i==6):
			print "%d"%(regmxfo(m,n,o,p,s,'mx'))
		elif(i==2):
			print "%d"%(regweb(m,n,o,p,s))
		elif(i==4):
			print "%d"%(regmob(m,n,o,p,s))
		elif(i==3):
			print "%d"%(regapp(m,n,o,p,s))
		print ""
	elif(t==2): #Unregistered Users
		i = int(raw_input("\n1 - All Platforms\n2 - Scandid Web\n3 - Mobile App\n4 - Mobile Web Browser\n5 - First Offer\n6 - Micromax\n"))
		m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
		o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
		print ""
		if(i==1):
			print "%d"%(unregall(m,n,o,p,s))
		elif(i==5):
			print "%d"%(unregmxfo(m,n,o,p,s,'fo'))
		elif(i==6):
			print "%d"%(unregmxfo(m,n,o,p,s,'mx'))
		elif(i==2):
			print "%d"%(unregweb(m,n,o,p,s))
		elif(i==4):
			print "%d"%(unregmob(m,n,o,p,s))
		elif(i==3):
			print "%d"%(unregapp(m,n,o,p,s))
		print ""
	elif(t==3): #All Users
		i = int(raw_input("\n1 - All Platforms\n2 - Scandid Web\n3 - Mobile App\n4 - Mobile Web Browser\n5 - First Offer\n6 - Micromax\n"))
		m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
		o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
		print ""
		if(i==1):
			print "%d"%(regall(m,n,o,p,s)+unregall(m,n,o,p,s))
		elif(i==5):
			print "%d"%(regmxfo(m,n,o,p,s,'fo')+unregmxfo(m,n,o,p,s,'fo'))
		elif(i==6):
			print "%d"%(regmxfo(m,n,o,p,s,'mx')+unregmxfo(m,n,o,p,s,'mx'))
		elif(i==2):
			print "%d"%(unregweb(m,n,o,p,s)+regweb(m,n,o,p,s))
		elif(i==4):
			print "%d"%(unregmob(m,n,o,p,s)+regmob(m,n,o,p,s))
		elif(i==3):
			print "%d"%(unregapp(m,n,o,p,s)+regapp(m,n,o,p,s))
		print ""
db.commit()
