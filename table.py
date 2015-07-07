import MySQLdb as mdb
db = mdb.connect('localhost','admin','scandid321','scandid')
c = db.cursor()
t = 1
while (t==1):
	print "Press accordingly :"
	print "1 - Create a new table"
	print "2 - Loading data(CSV) into a table"
	print "3 - Truncate i.e. delete all the records in the table"
	print "4 - Delete an existing table"
	print "5 - Show columns of an existing table"
	print "6 - Show all tables in the database"
	print "7 - Alter an existing table"
	print "0 - Exit"
	i = int(raw_input())
	if(i==1): #Create a new table
		s = raw_input("Enter the name of the new table.\n")
		flag = int(raw_input("Press 1 if you want the default table or 2 if you want to create your own.\n"))
		if(flag==1): #Default table according to the Activity Log
			q1 = """CREATE TABLE %s(month varchar(5),date int,entry time,a varchar(700), b varchar(700),thru varchar(700),session varchar(700),site varchar(700),browser varchar(700),ip varchar(200),mode varchar(700),code varchar(700))"""%(s)
			c.execute(q1)
		elif(flag==2):	#Customised Table
			temp = int(raw_input("Enter the number of columns.\n"))
			j = 1
			while(j<=temp):
				a,b = raw_input("Enter 'Name of column'' ''Type of column'\n").split()
				if(j==1):
					q1 = """CREATE TABLE %s(%s %s)"""%(s,a,b)
					c.execute(q1)
				else:
					q2 = """ALTER TABLE %s ADD %s %s"""%(s,a,b) #Adding new columns
					c.execute(q2)
				j = j + 1
		print "\nThe table '%s' has been created as follows:\n"%(s)
		q1 = """DESCRIBE %s"""%(s) #Displaying table data
		c.execute(q1)
		res = c.fetchall()
		print "Field\tType\tNull\tKey\tDefault\tExtra"
		for row in res:
			j1 = row[0]
			j2 = row[1]
			j3 = row[2]
			j4 = row[3]
			j5 = row[4]
			j6 = row[5]
			print "%s\t%s\t%s\t%s\t%s\t%s"%(j1,j2,j3,j4,j5,j6)
		print "\n"
	elif(i==2): #Loading Data(CSV) into the table
		dir = "C:/Users/akhilg/Desktop"
		temp = 1
		while (temp==1):
			b = int(raw_input("The current directory is %s.\nIf you want to change it, press 1, else press 0.\n"%(dir)))
			if(b==1): #Change the directory
				dir = raw_input("Enter the full path of the new directory.\n")
			a,y = raw_input("Enter the name of the CSV file and the table.\n").split()
			q1 = """LOAD DATA LOCAL INFILE '%s/%s.csv' INTO TABLE %s FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'""" %(dir,a,y)
			c.execute(q1)
			p = raw_input("\nYour data has been loaded.\nPress Y if you want to load more files, else press N.\n")
			if(p=="N"):
				temp = 2
				break
	elif(i==3): #Truncate the data from the table
		print "The selected database has the following tables:\n"
		q1 = """SHOW TABLES"""
		try :
			c.execute(q1)
			res = c.fetchall()
			for row in res:
				r = row[0]
				print "%s"%(r)
		except :
			print "No table found!"
		s = raw_input("\nEnter the name of the table whose data you want to truncate.\n")
		n = raw_input("Are you sure? (Y/N)\n")
		if(n=="Y"):
			q2 = """TRUNCATE TABLE %s"""%(s)
			c.execute(q2)
			print "\nThe data has been truncated and the table '%s' is empty.\n"%(s)
	elif(i==4): #Delete a table from the database 'scandid'
		print "The selected database has the following tables:\n"
		q1 = """SHOW TABLES"""
		try :
			c.execute(q1)
			res = c.fetchall()
			for row in res:
				r = row[0]
				print "%s"%(r)
		except :
			print "No table found!"
		s = raw_input("\nEnter the name of the table to be deleted.\n")
		n = raw_input("Are you sure? (Y/N)\n")
		if(n=="Y"):
			q2 = """DROP TABLE %s"""%(s)
			c.execute(q2)
			print "\nThe table '%s' has been deleted.\n"%(s)
	elif(i==5): #Displaying columns of a table
		s = raw_input("Enter the name of the table.\n")
		print "\nThe table '%s' has following columns :\n"%(s)
		q1 = """DESCRIBE %s"""%(s)
		c.execute(q1)
		res = c.fetchall()
		print "Field\tType\tNull\tKey\tDefault\tExtra"
		for row in res:
			j1 = row[0]
			j2 = row[1]
			j3 = row[2]
			j4 = row[3]
			j5 = row[4]
			j6 = row[5]
			print "%s\t%s\t%s\t%s\t%s\t%s"%(j1,j2,j3,j4,j5,j6)
		print "\n"
	elif(i==6): #Displaying all the tables in the database 'scandid'
		q1 = """SELECT DATABASE()"""
		c.execute(q1)
		res = c.fetchall()
		for row in res:
			a = row[0]
		print "The selected database '%s' has the following tables:\n"%(a)
		q2 = """SHOW TABLES"""
		c.execute(q2)
		res = c.fetchall()
		for row in res:
			r = row[0]
			print "%s"%(r)
		print ""
	elif(i==7): #Alter a table
		s = raw_input("Enter the name of the table.\n")
		print "Press accordingly :"
		print "1 - Change Column Name/Type"
		print "2 - Add Index"
		print "3 - Delete Index"
		b = int(raw_input())
		if(b==1): #Changing Column Name/Type
			q1 = """DESCRIBE %s"""%(s)
			c.execute(q1)
			res = c.fetchall()
			print "The table '%s' has the following fields:"%(s)
			print "Field\tType\tNull\tKey\tDefault\tExtra"
			for row in res:
				j1 = row[0]
				j2 = row[1]
				j3 = row[2]
				j4 = row[3]
				j5 = row[4]
				j6 = row[5]
				print "%s\t%s\t%s\t%s\t%s\t%s"%(j1,j2,j3,j4,j5,j6)
			m = raw_input("\nEnter the field you want to change.\n")
			n,o = raw_input("\nEnter the new field name and the type.\n").split()
			q2 = """ALTER TABLE %s CHANGE %s %s %s"""%(s,m,n,o)
			c.execute(q2)
			print "The intended change has been made.\n"
		elif(b==2): #Add Index
			q1 = """DESCRIBE %s"""%(s)
			c.execute(q1)
			res = c.fetchall()
			print "The table '%s' has the following fields:"%(s)
			print "Field\tType\tNull\tKey\tDefault\tExtra"
			for row in res:
				j1 = row[0]
				j2 = row[1]
				j3 = row[2]
				j4 = row[3]
				j5 = row[4]
				j6 = row[5]
				print "%s\t%s\t%s\t%s\t%s\t%s"%(j1,j2,j3,j4,j5,j6)
			a = raw_input("\nEnter the name of the column which is to be indexed.\n")
			b = raw_input("\nEnter the name of the index.\n")
			q2 = """ALTER TABLE %s ADD INDEX %s(%s)"""%(s,b,a)
			c.execute(q2)
			print "The index '%s' to '%s' has been added.\n"%(b,a)
		elif(b==3): #Delete Index
			print "The table '%s' has the following indexes:\n"%(s)
			q1 = """SHOW INDEX FROM %s"""%(s)
			c.execute(q1)
			print "Column\tIndex"
			res = c.fetchall()
			for row in res:
				j1 = row[2]
				j2 = row[4]
				print "%s\t%s"%(j1,j2)
			a = raw_input("\nEnter the name of the index to be deleted.\n")
			q2 = """DROP INDEX %s ON %s"""%(t,s)
			c.execute(q2)
			print "\nThe intended change has been made.\n"
	elif(i==0): #Exit
		t = 2
		break
db.commit()
