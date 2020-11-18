import MySQLdb
import os



db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="khalil",         # your username
                     passwd="123456",  # your password
                     db="stage",
                     charset='utf8')        # name of the data base

mycursor = db.cursor()
mycursor.execute("TRUNCATE TABLE lienExternes")
db.commit()
 

os.system('python stage.py')
os.system('python indeed.py')


mycursor.execute("INSERT INTO lienExternes SELECT * FROM temp")
mycursor.execute("TRUNCATE TABLE temp")
db.commit()