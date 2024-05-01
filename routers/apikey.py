from fastapi import APIRouter, HTTPException, Body
from models.apikey import APIKey
from settings.dbconnection import db
from settings.cryptography import encrypt, decrypt
import subprocess, time, datetime, json, requests

router = APIRouter()
#CREATE
@router.post('/apikeys')
def create_product(token: str = Body(), apikey: APIKey = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=401, detail="Access not found")
	sql="INSERT INTO apikeys (userid,passwdid,user)VALUE(%s,%s,%s);"
	adr = (encrypt(apikey.user),encrypt(apikey.passwd),myresult["id"])
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"apikey": cursorObj.lastrowid}
#UPDATE
@router.put('/apikeys/')
def update_user(token: str = Body(), id: int = Body(), apikey: APIKey = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=401, detail="Access not found")
	sql="UPDATE apikeys SET userid=%s,passwd=%s WHERE id=%s AND user=%s"
	adr = (encrypt(apikey["user"]),encrypt(apikey["passwd"]),id, myresult["id"])
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"apikey": id}
#READ
@router.get('/apikeys')
def get_users(token: str = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=401, detail="Access not found")
	sql="SELECT id, userid as user, passwdid as password FROM apikeys WHERE user=%s"
	adr = (myresult["id"], )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	for x in myresult:
		x["user"]=decrypt(x["user"])
		x["password"]=decrypt(x["password"])
	conn.close()
	return myresult
#DELETE
@router.delete('/apikeys/')
def del_user(token: str = Body(), id: int = Body(gt=0)):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=401, detail="Access not found")
	sql="DELETE FROM apikeys WHERE id=%s AND user=%s"
	adr = (id, myresult["id"])
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"apikey": id}
