import MySQLdb as mdb #Proofread and AllUsers!
db = mdb.connect('localhost','admin','scandid321','scandid')
c = db.cursor()
map = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
days = [31,28,31,30,31,30,31,31,30,31,30,31]
seconds = [0,10,60,180,600,1800,3600,10800,36000,86400,259200,864000];
def dur(m1,d1,t1,m2,d2,t2): #(month,date,time)-start and (month,date,time)-end
	day = hrs = mins = secs = hr1 = hr2 = min1 = min2 = sec1 = sec2 = 0
	j = 0
	while(j<12):
		if(m1==map[j]):
			mo1 = j + 1
		if(m2==map[j]):
			mo2 = j + 1
		j = j + 1
	count = 0
	t3 = str(t1)
	t4 = str(t2)
	for st in t3:
		if(st==":"):
			count = count + 1;
		else:
			if(count==0):
				hr1 = hr1*10 + int(st)
			elif(count==1):
				min1 = min1*10 + int(st)
			elif(count==2):
				sec1 = sec1*10 + int(st)
	count = 0
	for st in t4:
		if(st==":"):
			count = count + 1;
		else:
			if(count==0):
				hr2 = hr2*10 + int(st)
			elif(count==1):
				min2 = min2*10 + int(st)
			elif(count==2):
				sec2 = sec2*10 + int(st)
	#mo1,d1,hr1,min1,sec1 for start entry and mo2,d2,hr2,min2,sec2 for end entry
	if(mo1==mo2):
		if(d1==d2):
			if(hr1==hr2):
				if(min1==min2):
					if(sec1==sec2):
						ans = 0
					else:
						ans = sec2 - sec1
				else:
					ans = (60 - sec1) + sec2 + (min2 - min1 - 1)*60
			else:
				ans = (hr2 - hr1 - 1)*60*60 + (59 - min1 + min2)*60 + (60 - sec1 + sec2)
		else:
			ans = (d2 - d1 - 1)*24*60*60 + (23 - hr1 + hr2)*60*60 + (59 - min1 + min2)*60 + (60 - sec1 + sec2)
	else:
		ans = (23 - hr1 + hr2)*60*60 + (59 - min1 + min2)*60 + (60 - sec1 + sec2)
		day = days[mo1-1] - d1
		mo1 = mo1 + 1
		while(mo1<mo2):
			day = day + days[mo1-1]
			mo = mo + 1
		day = day + d2 - 1
		ans = ans + day*24*60*60
	j = 0
	while(j<12):
		if(ans>=seconds[j]):
			j = j + 1
		else:
			return j-1;
			break
	if(j==12):
		return j-1;
def unregall(m,n,o,p,s,c_ses,final,max): #Unregistered Users - All Platforms
	u = int(n)
	v = int(p)
	a = []
	b = [0]*100000
	flag = 0
	if(u==v):
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s)	
	c.execute(q)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	j = 0
	while(j<flag):
		final[b[j]] = final[b[j]] + 1
		if(b[j]>max[0]):
			max[0] = b[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return flag
def regall(m,n,o,p,s,c_ses,final,max): #Registered Users - All Platforms
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	fla = 0
	a = []
	b = [0]*100000
	d = []
	e = []
	i = []
	ses = []
	check = []
	res = c.fetchall()
	for row in res:
		d.append(row[0])
		e.append(row[1])
		i.append(0)
		fla = fla + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	z = 0
	foo = 0
	while(z<flag):
		p = a[z]
		j = 0
		while(j<fla):
			if(p==d[j]):
				if(i[j]==0):
					ses.append(e[j])
					check.append(b[z])
					foo = foo + 1
					i[j] = 1
					t = e[j]
					yy = j - 1
					if(yy>=0):
						while(e[yy]==t):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					zz = j + 1
					if(zz<flag):
						while(e[zz]==t):
							i[zz] = 1
							zz = zz + 1
							if(zz>=flag):
								break
				elif(i[j]==1):
					ii = 0
					while(ii<foo):
						if(ses[ii]==e[j]):
							check[ii] = check[ii] + b[z]
							break
						ii = ii + 1
				break
			j = j + 1
		z = z + 1
	j = 0
	while(j<foo):
		final[check[j]] = final[check[j]] + 1
		if(check[j]>max[0]):
			max[0] = check[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return foo
def unregmxfo(m,n,o,p,s,x,c_ses,final,max): #Unregistered Users - Micromax/First Offer
	u = int(n)
	v = int(p)
	a = []
	b = [0]*100000
	flag = 0
	if(u==v):
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(s,map[u-1],int(m),int(o),x,s)
	else:
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],x,s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],x,s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),x,s)	
	c.execute(q)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	j = 0
	while(j<flag):
		final[b[j]] = final[b[j]] + 1
		if(b[j]>max[0]):
			max[0] = b[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return flag
def regmxfo(m,n,o,p,s,x,c_ses,final,max): #Registered Users - Micromax/First Offer
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	fla = 0
	a = []
	b = [0]*100000
	d = []
	e = []
	i = []
	ses = []
	check = []
	res = c.fetchall()
	for row in res:
		d.append(row[0])
		e.append(row[1])
		i.append(0)
		fla = fla + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(s,map[u-1],int(m),int(o),x,s,map[u-1],int(m),int(o),x)
	else:
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' " %(s,map[u-1],int(m),days[u-1],x,s,map[u-1],int(m),days[u-1],x)
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' "%(map[u-1],1,days[u-1],x,s,map[u-1],1,days[u-1],x)
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = '%s' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),x,s,map[u-1],1,int(o),x)
	c.execute(q1)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	z = 0
	foo = 0
	while(z<flag):
		p = a[z]
		j = 0
		while(j<fla):
			if(p==d[j]):
				if(i[j]==0):
					ses.append(e[j])
					check.append(b[z])
					foo = foo + 1
					i[j] = 1
					t = e[j]
					yy = j - 1
					if(yy>=0):
						while(e[yy]==t):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					zz = j + 1
					if(zz<flag):
						while(e[zz]==t):
							i[zz] = 1
							zz = zz + 1
							if(zz>=flag):
								break
				elif(i[j]==1):
					ii = 0
					while(ii<foo):
						if(ses[ii]==e[j]):
							check[ii] = check[ii] + b[z]
							break
						ii = ii + 1
				break
			j = j + 1
		z = z + 1
	j = 0
	while(j<foo):
		final[check[j]] = final[check[j]] + 1
		if(check[j]>max[0]):
			max[0] = check[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return foo
def unregweb(m,n,o,p,s,c_ses,final,max): #Unregistered Users - Scandid Web
	u = int(n)
	v = int(p)
	a = []
	b = [0]*100000
	flag = 0
	if(u==v):
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,int(o),s)	
	u = int(n)
	v = int(p)
	if(u==v):
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s)
	else:
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE 'sw/apps%%' AND THRU NOT LIKE 'sw/api%%' AND THRU NOT LIKE '%%/mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s)
	c.execute(q)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	j = 0
	while(j<flag):
		final[b[j]] = final[b[j]] + 1
		if(b[j]>max[0]):
			max[0] = b[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])	
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return flag
def unregmob(m,n,o,p,s,c_ses,final,max): #Unregistered Users - Mobile Web Browser
	u = int(n)
	v = int(p)
	a = []
	b = [0]*100000
	flag = 0
	if(u==v):
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,int(o),s)	
	u = int(n)
	v = int(p)
	if(u==v):
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s)
	else:
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s)
	c.execute(q)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	j = 0
	while(j<flag):
		final[b[j]] = final[b[j]] + 1
		if(b[j]>max[0]):
			max[0] = b[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return flag
def unregapp(m,n,o,p,s,c_ses,final,max): #Unregistered Users - Mobile App
	u = int(n)
	v = int(p)
	a = []
	b = [0]*100000
	flag = 0
	if(u==v):
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),int(o),s)
	else:
		q = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(s,map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,int(o),s)	
	u = int(n)
	v = int(p)
	if(u==v):
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s)
	else:
		q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') " %(map[u-1],int(m),days[u-1],s)
		u = u + 1
		while(u<v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') "%(map[u-1],1,days[u-1],s)
			u = u + 1
		if(u==v):
			q = q + "OR SESSION LIKE 'provisionalid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) NOT IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s)
	c.execute(q)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	j = 0
	while(j<flag):
		final[b[j]] = final[b[j]] + 1
		if(b[j]>max[0]):
			max[0] = b[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return flag
def regweb(m,n,o,p,s,c_ses,final,max): #Registered Users - Scandid Web
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	fla = 0
	a = []
	b = [0]*100000
	d = []
	e = []
	i = []
	ses = []
	check = []
	res = c.fetchall()
	for row in res:
		d.append(row[0])
		e.append(row[1])
		i.append(0)
		fla = fla + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' " %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidweb' "%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' " %(map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'sw%%' AND THRU NOT LIKE '%%apps%%' AND THRU NOT LIKE '%%api%%' AND THRU NOT LIKE '%%/mobile%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	z = 0
	foo = 0
	while(z<flag):
		p = a[z]
		j = 0
		while(j<fla):
			if(p==d[j]):
				if(i[j]==0):
					ses.append(e[j])
					check.append(b[z])
					foo = foo + 1
					i[j] = 1
					t = e[j]
					yy = j - 1
					if(yy>=0):
						while(e[yy]==t):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					zz = j + 1
					if(zz<flag):
						while(e[zz]==t):
							i[zz] = 1
							zz = zz + 1
							if(zz>=flag):
								break
				elif(i[j]==1):
					ii = 0
					while(ii<foo):
						if(ses[ii]==e[j]):
							check[ii] = check[ii] + b[z]
							break
						ii = ii + 1
				break
			j = j + 1
		z = z + 1
	j = 0
	while(j<foo):
		final[check[j]] = final[check[j]] + 1
		if(check[j]>max[0]):
			max[0] = check[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return foo
def regmob(m,n,o,p,s,c_ses,final,max): #Registered Users - Mobile Web Browser	
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	fla = 0
	a = []
	b = [0]*100000
	d = []
	e = []
	i = []
	ses = []
	check = []
	res = c.fetchall()
	for row in res:
		d.append(row[0])
		e.append(row[1])
		i.append(0)
		fla = fla + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' " %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'scandidmobilesite' "%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' " %(map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU LIKE 'mobile%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	z = 0
	foo = 0
	while(z<flag):
		p = a[z]
		j = 0
		while(j<fla):
			if(p==d[j]):
				if(i[j]==0):
					ses.append(e[j])
					check.append(b[z])
					foo = foo + 1
					i[j] = 1
					t = e[j]
					yy = j - 1
					if(yy>=0):
						while(e[yy]==t):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					zz = j + 1
					if(zz<flag):
						while(e[zz]==t):
							i[zz] = 1
							zz = zz + 1
							if(zz>=flag):
								break
				elif(i[j]==1):
					ii = 0
					while(ii<foo):
						if(ses[ii]==e[j]):
							check[ii] = check[ii] + b[z]
							break
						ii = ii + 1
				break
			j = j + 1
		z = z + 1
	j = 0
	while(j<foo):
		final[check[j]] = final[check[j]] + 1
		if(check[j]>max[0]):
			max[0] = check[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return foo
def regapp(m,n,o,p,s,c_ses,final,max): #Registered Users - Mobile App
	q = "SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5) FROM %s WHERE SESSION LIKE 'prodfileid%%' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'prodfileid')+11,5)" %(s)
	c.execute(q)
	flag = 0
	fla = 0
	a = []
	b = [0]*100000
	d = []
	e = []
	i = []
	ses = []
	check = []
	res = c.fetchall()
	for row in res:
		d.append(row[0])
		e.append(row[1])
		i.append(0)
		fla = fla + 1
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' " %(s,map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = "SELECT MONTH,DATE,ENTRY,SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26),SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26) FROM %s WHERE SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' " %(s,map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = 'mobile' "%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	u = int(n)
	v = int(p)
	if(u==v):
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)" %(map[u-1],int(m),int(o),s,map[u-1],int(m),int(o))
	else:
		q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' " %(map[u-1],int(m),days[u-1],s,map[u-1],int(m),days[u-1])
		u = u + 1
		while(u<v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' "%(map[u-1],1,days[u-1],s,map[u-1],1,days[u-1])
			u = u + 1
		if(u==v):
			q1 = q1 + "OR SESSION LIKE 'prodfileid%%' AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' OR SESSION LIKE 'provisionalid%%' AND SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) IN (SELECT DISTINCT SUBSTR(SESSION,INSTR(SESSION,'provisionalid')+14,26) FROM %s WHERE SESSION LIKE 'prodfileid%%') AND MONTH = '%s' AND DATE BETWEEN '%d' AND '%d' AND MODE = ' ' AND THRU REGEXP 'apps|api|/mobile' ORDER BY SUBSTR(SESSION,INSTR(SESSION,'sessionid')+10,26)"%(map[u-1],1,int(o),s,map[u-1],1,int(o))
	c.execute(q1)
	temp = 0
	res = c.fetchall()
	xx = c.rowcount
	for r in res:
		if(temp==0):
			m1 = m2 = r[0]
			d1 = d2 = r[1]
			t1 = t2 = r[2]
			prev = r[4]
			prev_pro = r[3]
			temp = 1
		elif(temp==1):
			if(r[4]==prev):
				m2 = r[0]
				d2 = r[1]
				t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
			else:
				goo = dur(m1,d1,t1,m2,d2,t2)
				c_ses[goo] = c_ses[goo] + 1
				j = 0
				while(j<flag):
					if(a[j]==prev_pro):
						b[j] = b[j] + 1
						j = -1
						break
					j = j + 1
				if(j==flag):
					a.append(prev_pro)
					b[flag] = 1
					flag = flag + 1
				m1 = m2 = r[0]
				d1 = d2 = r[1]
				t1 = t2 = r[2]
				prev = r[4]
				prev_pro = r[3]
	if(xx>0):
		goo = dur(m1,d1,t1,m2,d2,t2)
		c_ses[goo] = c_ses[goo] + 1
	j = 0
	while(j<flag):
		if(a[j]==prev_pro):
			b[j] = b[j] + 1
			j = -1
			break
		j = j + 1
	if((j==flag)&(xx>0)):
		a.append(prev_pro)
		b[flag] = 1
		flag = flag + 1
	z = 0
	foo = 0
	while(z<flag):
		p = a[z]
		j = 0
		while(j<fla):
			if(p==d[j]):
				if(i[j]==0):
					ses.append(e[j])
					check.append(b[z])
					foo = foo + 1
					i[j] = 1
					t = e[j]
					yy = j - 1
					if(yy>=0):
						while(e[yy]==t):
							i[yy] = 1
							yy = yy - 1
							if(yy<0):
								break
					zz = j + 1
					if(zz<flag):
						while(e[zz]==t):
							i[zz] = 1
							zz = zz + 1
							if(zz>=flag):
								break
				elif(i[j]==1):
					ii = 0
					while(ii<foo):
						if(ses[ii]==e[j]):
							check[ii] = check[ii] + b[z]
							break
						ii = ii + 1
				break
			j = j + 1
		z = z + 1
	j = 0
	while(j<foo):
		final[check[j]] = final[check[j]] + 1
		if(check[j]>max[0]):
			max[0] = check[j]
		j = j + 1
	"""print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
	j = 1
	while(j<=max):
		if(final[j]!=0):
			print "%d - %d"%(j,final[j])
		j = j + 1"""
	return foo
def showtable(): #Show Tables
	q1 = "SHOW TABLES"
	c.execute(q1)
	res = c.fetchall()
	print "The database 'scandid' has the following tables:\n"
	for r in res:
		a = r[0]
		print "%s"%(a)
def maxoftwo(a,b): #Maximum of two numbers
	if(a>=b):
		return a
	else:
		return b
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
		c_ses = [0]*100
		final = [0]*100000
		max = [0]
		print ""
		if(i==1):
			w = regall(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==5):
			w = regmxfo(m,n,o,p,s,'fo',c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==6):
			w = regmxfo(m,n,o,p,s,'mx',c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==2):
			w = regweb(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==4):
			w = regmob(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==3):
			w = regapp(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		print ""
	elif(t==2): #Unregistered Users
		i = int(raw_input("\n1 - All Platforms\n2 - Scandid Web\n3 - Mobile App\n4 - Mobile Web Browser\n5 - First Offer\n6 - Micromax\n"))
		m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
		o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
		print ""
		c_ses = [0]*100
		final = [0]*100000
		max = [0]
		if(i==1):
			w = unregall(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==5):
			w = unregmxfo(m,n,o,p,s,'fo',c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==6):
			w = unregmxfo(m,n,o,p,s,'mx',c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==2):
			w = unregweb(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==4):
			w = unregmob(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==3):
			w = unregapp(m,n,o,p,s,c_ses,final,max)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(c_ses[0],c_ses[1],c_ses[2],c_ses[3],c_ses[4],c_ses[5],c_ses[6],c_ses[7],c_ses[8],c_ses[9],c_ses[10],c_ses[11])
			j = 1
			while(j<=max[0]):
				if(final[j]!=0):
					print "The number of users with %d sessions are %d."%(j,final[j])
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		print ""
	elif(t==3): #All Users
		i = int(raw_input("\n1 - All Platforms\n2 - Scandid Web\n3 - Mobile App\n4 - Mobile Web Browser\n5 - First Offer\n6 - Micromax\n"))
		m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
		o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
		print ""
		a_ses = [0]*100
		b_ses = [0]*100
		final1 = [0]*100000
		final2 = [0]*100000
		max1 = [0]
		max2 = [0]
		if(i==1):
			w = unregall(m,n,o,p,s,a_ses,final1,max1) + regall(m,n,o,p,s,b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==2):
			w = unregweb(m,n,o,p,s,a_ses,final1,max1) + regweb(m,n,o,p,s,b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==3):
			w = unregapp(m,n,o,p,s,a_ses,final1,max1) + regapp(m,n,o,p,s,b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==4):
			w = unregmob(m,n,o,p,s,a_ses,final1,max1) + regmob(m,n,o,p,s,b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==5):
			w = unregmxfo(m,n,o,p,s,'fo',a_ses,final1,max1) + regmxfo(m,n,o,p,s,'fo',b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		elif(i==6):
			w = unregmxfo(m,n,o,p,s,'mx',a_ses,final1,max1) + regmxfo(m,n,o,p,s,'mx',b_ses,final2,max2)
			print "0 to 10 seconds - %d\n10 seconds to 1 minute - %d\n1 minute to 3 minutes - %d\n3 minutes to 10 minutes - %d\n10 minutes to 30 minutes - %d\n30 minutes to 1 hour - %d\n1 hour to 3 hours - %d\n3 hours to 10 hours - %d\n10 hours to 1 day - %d\n1 day to 3 days - %d\n3 days to 10 days - %d\nMore than 10 days - %d\n"%(a_ses[0]+b_ses[0],a_ses[1]+b_ses[1],a_ses[2]+b_ses[2],a_ses[3]+b_ses[3],a_ses[4]+b_ses[4],a_ses[5]+b_ses[5],a_ses[6]+b_ses[6],a_ses[7]+b_ses[7],a_ses[8]+b_ses[8],a_ses[9]+b_ses[9],a_ses[10]+b_ses[10],a_ses[11]+b_ses[11])
			j = 1
			while(j<=maxoftwo(max1[0],max2[0])):
				if((final1[j]+final2[j])!=0):
					print "The number of users with %d sessions are %d."%(j,(final1[j]+final2[j]))
				j = j + 1
			print "\nTotal Users : %d\n"%(w)
		print ""
db.commit()
