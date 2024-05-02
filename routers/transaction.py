from fastapi import APIRouter, HTTPException, Body, Header
from models.transaction import Transaction
from settings.dbconnection import db
from settings.cryptography import encrypt, decrypt
from datetime import datetime
import subprocess, time, datetime, json, requests

router = APIRouter()

@router.get('/transactions')
def get_transactions(token: str = Header()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql = "SELECT u.id, u.date, a.userid, a.passwdid, linkid FROM users u LEFT JOIN apikeys a ON a.user=u.id LEFT JOIN links l ON l.apikeys=a.id WHERE u.token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	now = time.time()
	conn.close()
	if not myresult or myresult[0]["date"] < now:
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	url="https://sandbox.belvo.com/api/transactions/?link="
	s = []
	for x in myresult:
		session.auth = (decrypt(x["userid"]),decrypt(x["passwdid"]))
		r = session.get(url+x["linkid"])
		if r.status_code>=200 and r.status_code < 300:
			s.append(json.loads(r.content))
	return s
#SERVICIOS
@router.get('/transactions/total')
def get_total(token: str = Header()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql = "SELECT u.id, u.date, a.userid, a.passwdid, linkid FROM users u LEFT JOIN apikeys a ON a.user=u.id LEFT JOIN links l ON l.apikeys=a.id WHERE u.token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	now = time.time()
	conn.close()
	if not myresult or myresult[0]["date"] < now:
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	url="https://sandbox.belvo.com/api/transactions/?link="
	s = 0.0
	for x in myresult:
		session.auth = (decrypt(x["userid"]),decrypt(x["passwdid"]))
		r = session.get(url+x["linkid"])
		if r.status_code>=200 and r.status_code < 300:
			i=json.loads(r.content)
			for y in i["results"]:
				s += y["balance"]
	return s
@router.get('/transactions/amounts')
def get_amounts(token: str = Header()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql = "SELECT u.id, u.date, a.userid, a.passwdid, linkid FROM users u LEFT JOIN apikeys a ON a.user=u.id LEFT JOIN links l ON l.apikeys=a.id WHERE u.token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	now = time.time()
	conn.close()
	if not myresult or myresult[0]["date"] < now:
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	url="https://sandbox.belvo.com/api/transactions/?link="
	s = 0.0
	for x in myresult:
		session.auth = (decrypt(x["userid"]),decrypt(x["passwdid"]))
		r = session.get(url+x["linkid"])
		if r.status_code>=200 and r.status_code < 300:
			i=json.loads(r.content)
			for y in i["results"]:
				s += y["amount"]
	return s
@router.get('/transactions/financial_health')
def get_financial_health(token: str = Header()):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql = "SELECT u.id, u.date, a.userid, a.passwdid, linkid FROM users u LEFT JOIN apikeys a ON a.user=u.id LEFT JOIN links l ON l.apikeys=a.id WHERE u.token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	now = time.time()
	conn.close()
	if not myresult or myresult[0]["date"] < now:
		raise HTTPException(status_code=401, detail="Access not found")
	session = requests.Session()
	url="https://sandbox.belvo.com/api/transactions/?link="
	s = 0.0
	a = 0.0
	for x in myresult:
		session.auth = (decrypt(x["userid"]),decrypt(x["passwdid"]))
		r = session.get(url+x["linkid"])
		if r.status_code>=200 and r.status_code < 300:
			i=json.loads(r.content)
			for y in i["results"]:
				s += y["balance"]
				a += y["amount"]
	health = s > a
	return {"ingress": s, "egress": a, "health": health}
