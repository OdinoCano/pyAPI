from fastapi import APIRouter, HTTPException, Body, Header
from models.link import Link
from settings.dbconnection import db
from settings.cryptography import encrypt, decrypt
from datetime import datetime
import subprocess, time, json, requests

router = APIRouter()
#CREATE
@router.post('/links')
def create_product(token: str = Body(), link: Link = Body()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT u.id, u.date, a.userid, a.passwdid FROM users u LEFT JOIN apikeys a ON a.user=u.id WHERE u.token=%s AND a.id=%s"
	adr = (token, link.apikey)
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	session.auth = (decrypt(myresult["userid"]),decrypt(myresult["passwdid"]))
	url = "https://sandbox.belvo.com/api/links/"
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}
	json_body = {
		"institution": link.institution,
		"username": link.user
	}
	if link.passwd:
		json_body["password"] = link.passwd
	r = session.post(url, headers=headers, json=json_body)
	if r.status_code<200 and r.status_code>299:
		conn.close()
		raise HTTPException(status_code=404, detail="Server not found")
	s = json.loads(r.content)
	last = datetime.strptime(s["last_accessed_at"].split('.')[0], '%Y-%m-%dT%H:%M:%S').date().strftime("%s")
	created = datetime.strptime(s["created_at"].split('.')[0], '%Y-%m-%dT%H:%M:%S').date().strftime("%s")
	if link.passwd:
		sql="INSERT INTO links (linkid,status,institution,accessmode,apikeys,lastaccessedat,refreshrate,createdby,externalid,createdat,institutionuserid,user,passwd)VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		adr = (s["id"],s["status"],s["institution"],s["access_mode"],link.apikey,last,s["refresh_rate"],s["created_by"],s["external_id"],created,s["institution_user_id"],encrypt(link.user),encrypt(link.passwd))
	else:
		sql="INSERT INTO links (linkid,status,institution,accessmode,apikeys,lastaccessedat,refreshrate,createdby,externalid,createdat,institutionuserid,user)VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		adr = (s["id"],s["status"],s["institution"],s["access_mode"],link.apikey,last,s["refresh_rate"],s["created_by"],s["external_id"],created,s["institution_user_id"],encrypt(link.user))
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": cursorObj.lastrowid}
#UPDATE
@router.put('/links/')
def update_user(token: str = Body(), id: int = Body(), link: Link = Body()):
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
	sql="UPDATE links SET linkid=%s,apikeys=%s WHERE id=%s"
	adr = ('','',id)
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": id}
#READ
@router.get('/links')
def get_users(token: str = Header()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	#SELECT u.id, u.date, l.linkid, a.userid, a.passwdid FROM users u 
	#LEFT JOIN apikeys a ON a.user=u.id LEFT JOIN links l ON l.apikeys=a.id WHERE u.token=
	sql="SELECT u.id, u.date, a.userid, a.passwdid FROM users u LEFT JOIN apikeys a ON a.user=u.id WHERE u.token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	now = time.time()
	conn.close()
	if not myresult or myresult[0]["date"] < now:
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	url = "https://sandbox.belvo.com/api/links/"
	headers = {'accept': 'application/json'}
	s = []
	for x in myresult:
		session.auth = (decrypt(x["userid"]),decrypt(x["passwdid"]))
		r = session.get(url, headers=headers)
		if r.status_code>=200 and r.status_code < 300:
			s.append(json.loads(r.content))
	return s
#DELETE
@router.delete('/links/')
def del_user(token: str =Body(), id: int = Body(gt=0)):
	
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
	session = requests.Session()
	
	sql="DELETE FROM users WHERE id=%s"
	adr = (id, )
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"user": id}
