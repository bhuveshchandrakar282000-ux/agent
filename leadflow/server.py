import os,json,sqlite3,secrets,re
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).parent
DB=os.environ.get('LEADFLOW_DB',str(ROOT/'leads.db'))
TOKEN=os.environ.get('LEADFLOW_TOKEN') or secrets.token_urlsafe(24)
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init():
 with connect() as c:
  c.executescript('CREATE TABLE IF NOT EXISTS leads(id INTEGER PRIMARY KEY,name TEXT,email TEXT UNIQUE,company TEXT,budget INTEGER,message TEXT,score INTEGER,stage TEXT DEFAULT "New",followup TEXT DEFAULT "",created TEXT); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,lead_id INTEGER,description TEXT,created TEXT);')
def now():return datetime.now(timezone.utc).isoformat()
def score(budget,message):return min(100,20+(35 if budget>=1000 else 15 if budget>=300 else 0)+sum(15 for word in ['automation','integration','dashboard'] if word in message.lower()))
class Handler(BaseHTTPRequestHandler):
 def respond(self,status,data):
  raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def authorized(self):return secrets.compare_digest(self.headers.get('Authorization',''),'Bearer '+TOKEN)
 def do_GET(self):
  if self.path=='/':
   raw=(ROOT/'static/index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
  if self.path=='/health':return self.respond(200,{'ok':True})
  if not self.authorized():return self.respond(401,{'error':'Enter the server access token.'})
  with connect() as c:
   if self.path=='/api/leads':return self.respond(200,[dict(x) for x in c.execute('SELECT * FROM leads ORDER BY id DESC')])
   if self.path=='/api/events':return self.respond(200,[dict(x) for x in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 50')])
  self.respond(404,{'error':'Not found'})
 def do_POST(self):
  if not self.authorized():return self.respond(401,{'error':'Invalid token'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length<=0 or length>16384:return self.respond(400,{'error':'Invalid request size'})
   d=json.loads(self.rfile.read(length))
   if not isinstance(d,dict):raise ValueError('Expected an object')
   with connect() as c:
    if self.path=='/api/leads':
     name=str(d.get('name','')).strip()[:120];email=str(d.get('email','')).strip().lower()[:254];company=str(d.get('company','')).strip()[:120];message=str(d.get('message',''))[:2000];budget=int(d.get('budget',0))
     if not name or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email) or budget<0:raise ValueError('Valid name, email and nonnegative budget required')
     s=score(budget,message)
     cur=c.execute('INSERT INTO leads(name,email,company,budget,message,score,created) VALUES(?,?,?,?,?,?,?)',(name,email,company,budget,message,s,now()));lead_id=cur.lastrowid
     c.execute('INSERT INTO events(lead_id,description,created) VALUES(?,?,?)',(lead_id,f'Lead captured; rules score {s}/100',now()))
     return self.respond(201,{'id':lead_id,'score':s})
    if self.path=='/api/update':
     lead_id=int(d['id']);stage=d.get('stage','New');followup=str(d.get('followup',''))
     if stage not in ['New','Qualified','Contacted','Won','Lost']:raise ValueError('Invalid stage')
     if followup:datetime.strptime(followup,'%Y-%m-%d')
     cur=c.execute('UPDATE leads SET stage=?,followup=? WHERE id=?',(stage,followup,lead_id))
     if not cur.rowcount:return self.respond(404,{'error':'Lead not found'})
     c.execute('INSERT INTO events(lead_id,description,created) VALUES(?,?,?)',(lead_id,'Stage: '+stage+'; follow-up: '+(followup or 'none'),now()))
     return self.respond(200,{'ok':True})
   self.respond(404,{'error':'Not found'})
  except sqlite3.IntegrityError:self.respond(409,{'error':'This email already exists. No duplicate created.'})
  except (ValueError,KeyError,TypeError):self.respond(400,{'error':'Check your input fields.'})
if __name__=='__main__':
 init();print('LeadFlow: http://127.0.0.1:8000\nAccess token: '+TOKEN,flush=True);ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
