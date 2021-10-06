import sqlite3
con = sqlite3.connect('data.db')
cursor = con.cursor()

def CreateChatDB():
	cursor = con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS chats_aleks(chat_name TEXT, chat_id INT)") 
	con.commit()

def UpdateChatValue(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM chats_aleks where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE chats_aleks SET {val_name}={new} where id={id}")
		con.commit()

def InsertChatValues(chat_name, chat_id):
	cursor.execute(f'INSERT INTO chats_aleks VALUES ("{chat_name}", {chat_id})')
	con.commit()