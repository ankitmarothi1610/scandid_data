import operator
import MySQLdb as mdb
db = mdb.connect('localhost','scadmin','scandid321','fk')
c = db.cursor()
map = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
days = [31,28,31,30,31,30,31,31,30,31,30,31]
def day(odate): #returns distance of the odate from 1st Jan 2015
	month = ""
	date  = 0
	number_of_days = 0
	j = 1
	for x in odate:
		if((j>=5)&(j<=7)):
			month+=x
		elif(j==9):
			date = int(x)
		elif(j==10):	
			date = date*10 + int(x)
		j+=1
	if month in map:
		mon = map[month]
	u = 1
	if((mon<3)|(mon>6)):
		return 1000000
	while(u<mon):
		number_of_days+=days[u-1]
		u+=1
	number_of_days+=date
	return number_of_days
def sumofn(x):
	t = (x*(x+1))/2
	return t
def hotnessof(x):
	xx = ""
	for xxx in x:
		if(xxx=="'"):
			xx+="'"
		xx+=xxx #Escaping the "'" character
	q = "select * from trans where title = '%s' and status!= 'failed'"%(xx)
	c.execute(q)
	res = c.fetchall()
	available_EMA = [3,7,15,30,90]
	value_EMA = [0]*5
	for row in res:
		y = day(row[10])
		d = 31 + 28 + 31 + 30 + 31 + 30 + 1 - y
		j = 0
		for i in available_EMA:
			if((d<=i)&(d>0)):
				value_EMA[j]+=int(row[4])
			j = j + 1
	#print available_EMA
	#print value_EMA
	j = 4
	while(j>=0):
		if(value_EMA[j]!=0):
			break
		j = j - 1 #j has the highest non - zero value
	hotness = 0.0
	k = sumofn(j+1)
	flag = 0
	while(flag<=j):
		l = float(value_EMA[flag])/float(available_EMA[flag]) #imporve upon the weighted percentages
		m = float(j-flag+1)/k
		hotness+=l*m
		flag+=1 #calculating hotness
	return hotness
x = raw_input("Enter the name of the category.\n")
query = "select distinct title from trans where category = '%s' limit 300"%(x)
c.execute(query)
results = c.fetchall()
prod = {}
for row in results:
	prod[row[0]] = hotnessof(row[0])
sorted_prod = sorted(prod.items(),key = operator.itemgetter(1),reverse = True)
j = 1
for i in sorted_prod:
	print i
	if(j==100):
		break
	j = j + 1
db.commit()
db.close()
