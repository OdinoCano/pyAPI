from fastapi import APIRouter, HTTPException, Body
from models.apikey import APIKey
from settings.dbconnection import db
from settings.cryptography import encrypt, decrypt
import subprocess, time, datetime, json

router = APIRouter()
#CREATE
@router.post('/apikeys')
def create_product(token: str = Body(), user: APIKey = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT level, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if myresult["level"] > 1 and myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="INSERT INTO users (token,date,email,passwd,firstname,lastname)VALUE(%s,%s,%s,%s,%s,%s);"
	adr = ('', 1, user.email, user.passwd, user.firstName, user.lastName)
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": cursorObj.lastrowid}
#UPDATE
@router.put('/apikeys/')
def update_user(token: str = Body(), id: int = Body(), user: APIKey = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT level, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if myresult["level"] > 1 and myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="UPDATE users SET token=%s,date=%s,email=%s,passwd=%s,firstname=%s,lastname=%s WHERE id=%s"
	adr = ('', 1, user.email, user.passwd, user.firstName, user.lastName,id)
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": id}
#READ
@router.get('/apikeys')
def get_users():
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	cursorObj.execute("SELECT id, email, firstname, lastname FROM users")
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
#DELETE
@router.delete('/apikeys/')
def del_user(token: str =Body(), id: int = Body(gt=0)):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT level, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if myresult["level"] > 1 and myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="DELETE FROM users WHERE id=%s"
	adr = (id, )
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": id}
