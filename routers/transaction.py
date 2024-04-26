from fastapi import APIRouter, HTTPException, Query, Path
from models.transaction import Transaction
from settings.dbconnection import db
import subprocess, time, datetime, json

router = APIRouter()

@router.get('/transactions')
def get_transactions():
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	cursorObj.execute("SELECT t.id, t.concept, t.date, if(t.io=0,'INGRESS','EGRESS') as io, c.name as category, price FROM transactions t left join categories c ON c.id=t.category")
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
	
@router.get('/transactions/total')
def get_total():
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	cursorObj.execute("select SUM(IF(io=0,price,0)) as ingress, SUM(IF(io=1,price,0)) as egress from transactions")
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult

@router.get('/transactions/amounts')
def get_amounts(token: str):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	if not myresult:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="select c.name as category, t.price from transactions t left join categories c ON c.id=t.category order by category"
	cursorObj.execute(sql)
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
