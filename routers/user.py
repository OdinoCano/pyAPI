from fastapi import APIRouter, HTTPException, Query, Path
from models.user import User
from settings.dbconnection import db
import subprocess, time, datetime, json

router = APIRouter()
#ACCESS
@router.post('/users/')
def get_products_by_stock(user: str, passwd: str = Query(min_length=8, max_length=255)):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id FROM users WHERE email=%s AND passwd=%s"
	adr = (user, passwd)
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	if not myresult:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	cmd = ["openssl","rand","-hex","32"]
	returned_output = subprocess.check_output(cmd)
	token = returned_output.decode("utf-8").replace("\n", "")
	now = datetime.datetime.now()
	limit = datetime.timedelta(hours=4, minutes=46)
	expiration = int((limit + now).timestamp())
	sql = "UPDATE users SET token=%s, date=%s WHERE id=%s"
	adr = (token, expiration, myresult["id"])
	cursorObj.execute(sql, adr)
	conn.commit()
	conn.close()
	return {"token": token, "time": expiration}
#CREATE
@router.post('/users')
def create_product(token: str, user: User):
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
@router.put('/users/{id}')
def update_user(token: str, id: int, user: User):
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
@router.get('/users')
def get_users():
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	cursorObj.execute("SELECT id, email, firstname, lastname FROM users")
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
#DELETE
@router.delete('/users/{id}')
def del_user(token: str, id: int = Path(gt=0)):
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


#SERVICIOS
@router.get('/users/amounts')
def get_amounts(token: str):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="select c.name as category, t.price from transactions t left join categories c ON c.id=t.category WHERE user=%s order by category"
	adr = (myresult["id"], )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
@router.get('/users/financial_health')
def get_financial_health(token: str):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="select SUM(IF(io=0,price,0)) as ingress, SUM(IF(io=1,price,0)) as egress from transactions WHERE user=%s"
	adr = (myresult["id"], )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	health = myresult["ingress"] > myresult["egress"]
	conn.close()
	return {"ingress": myresult["ingress"], "egress": myresult["egress"], "health": health}
@router.get('/users/total')
def get_total(token: str):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="select SUM(IF(io=0,price,0)) as ingress, SUM(IF(io=1,price,0)) as egress from transactions WHERE user=%s"
	adr = (myresult["id"], )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	conn.close()
	return myresult
@router.get('/users/transactions')
def get_transactions(token: str):
	conn = db()
	cursorObj = conn.cursor(dictionary=True)
	sql="SELECT id, date FROM users WHERE token=%s"
	adr = (token, )
	cursorObj.execute(sql, adr)
	myresult = cursorObj.fetchone()
	now = time.time()
	if not myresult or myresult["date"] < now:
		conn.close()
		raise HTTPException(status_code=404, detail="Access not found")
	sql="SELECT t.id, t.concept, t.date, if(t.io=0,'INGRESS','EGRESS') as io, c.name as category, price FROM transactions t left join categories c ON c.id=t.category WHERE user=%s"
	adr = (myresult["id"], )
	cursorObj.execute(sql,adr)
	myresult = cursorObj.fetchall()
	conn.close()
	return myresult
