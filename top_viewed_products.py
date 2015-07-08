import operator
import MySQLdb as mdb #Proofread and AllUsers!
db = mdb.connect('localhost','admin','scandid321','scandid')
c = db.cursor()
map = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
days = [31,28,31,30,31,30,31,31,30,31,30,31]
#q = "select distinct noun from product"
#c.execute(q)
#res = c.fetchall()
dict = {}
#for r in res:
#	dict.setdefault(r[0],0)
s = raw_input("Enter the name of the table.\n")
m,n = raw_input("Enter the start date and month as 'DD MM'\n").split()
o,p = raw_input("Enter the end date and month as 'DD MM'\n").split()
u = int(n)
v = int(p)
if(u==v):
	q = "select distinct substr(session,instr(session,'productid')+10,instr(substr(session,instr(session,'productid')+10,100),',')-1) from %s where session like '%%provisionalid%%productid%%' and month = '%s' and date between '%d' and '%d'"%(s,map[u-1],int(m),int(o))
else:
	q = "select distinct substr(session,instr(session,'productid')+10,instr(substr(session,instr(session,'productid')+10,100),',')-1) from %s where session like '%%provisionalid%%productid%%' and month = '%s' and date between '%d' and '%d' "%(s,map[u-1],int(m),days[u-1])
	u+=1
	while(u<v):
		q = q + "or session like '%%provisionalid%%productid%%' and month = '%s' and date between '%d' and '%d' "%(map[u-1],1,days[u-1])
		u+=1
	q = q + "or session like '%%provisionalid%%productid%%' and month = '%s' and date between '%d' and '%d'"%(map[u-1],1,int(o))
c.execute(q)
res = c.fetchall()
count = 0
for r in res:
	q1 = "select noun from product where id = '%s'"%(r[0])
	c.execute(q1)
	results = c.fetchall()
	for row in results:
		s = row[0]
		if s not in dict:
			dict.setdefault(s,1)
			count+=1
		else:
			dict[s]+=1
			count+=1
d = sorted(dict.items(),key = operator.itemgetter(1),reverse = True)
for y in d:
	print y
print count
db.close()
