import unittest,tempfile,threading,json,urllib.request,urllib.error,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
class ApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();server.DB=cls.tmp.name+'/test.db';server.TOKEN='test-token';server.init();cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);threading.Thread(target=cls.http.serve_forever,daemon=True).start();cls.url='http://127.0.0.1:'+str(cls.http.server_port)
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.tmp.cleanup()
 def request(self,path,body=None,token='test-token'):
  req=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body is not None else None,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def test_workflow(self):
  self.assertEqual(self.request('/api/leads',token='wrong')[0],401)
  data={'name':'Demo','email':'DEMO@example.com','company':'Example','budget':1500,'message':'automation integration dashboard'}
  status,lead=self.request('/api/leads',data);self.assertEqual(status,201);self.assertEqual(lead['score'],100)
  data['email']='demo@example.com';self.assertEqual(self.request('/api/leads',data)[0],409)
  self.assertEqual(self.request('/api/update',{'id':lead['id'],'stage':'Won','followup':'2026-12-01'})[0],200)
  rows=self.request('/api/leads')[1];self.assertEqual(rows[0]['stage'],'Won');self.assertEqual(rows[0]['followup'],'2026-12-01')
  self.assertEqual(len(self.request('/api/events')[1]),2)
  self.assertEqual(self.request('/api/update',{'id':lead['id'],'stage':'Invalid'})[0],400)
  self.assertEqual(self.request('/api/leads',{'name':'Bad','email':'invalid','budget':-1})[0],400)
if __name__=='__main__':unittest.main()
