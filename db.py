import sqlite3
con = sqlite3.connect('data.db')
cursor = con.cursor()

def CreateDB():
	cursor = con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS aleks_bot(name TEXT, id INT, vip TEXT, dev TEXT)") 
	con.commit()

def UpdateValue(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM aleks_bot where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE aleks_bot SET {val_name}={new} where id={id}")
		con.commit()

def InsertValues(name, id):
	cursor.execute(f'INSERT INTO aleks_bot VALUES ("{name}", {id}, "off", "off")')
	con.commit()

def ReplaceValue(val_name, new_val, id):
		cursor.execute(f"UPDATE aleks_bot SET {val_name}={new_val} where id={id}")
		con.commit()

#for row in cursor.execute("SELECT money FROM aleks_bot ORDER BY money DESC"):
#	print(row[0])