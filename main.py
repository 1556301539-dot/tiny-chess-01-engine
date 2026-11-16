import json,os,sys,urllib.request,urllib.error
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000};N=(17,15,10,6,-6,-10,-15,-17);K8=(1,-1,8,-8,9,-9,7,-7);D={'r':(1,-1,8,-8),'b':(9,7,-9,-7),'q':(1,-1,8,-8,9,7,-9,-7)}
def pos(f):
 b={};x=f.split()[0].split('/')
 for r,z in enumerate(x):
  q=0
  for c in z:
   if c.isdigit():q+=int(c)
   else:b[(7-r)*8+q]=c;q+=1
 p=f.split();s='w' if len(p)<2 or p[1]=='w' else'b';c=p[2]if len(p)>2 else'-';e=p[3]if len(p)>3 else'-'
 return b,s,c,None if e=='-' else ord(e[0])-97+(int(e[1])-1)*8
def moves(b,s,ep):
 w=b[s].isupper();f=s%8;r=s//8;o=[]
 def put(t):
  if 0<=t<64 and abs(t%8-f)<=2 and (t not in b or b[t].isupper()!=w):o.append((t,''))
 x=b[s].lower()
 if x=='n':
  for d in N:
   t=s+d
   if 0<=t<64 and abs(t%8-f)<=2 and abs(t//8-r)<=2:put(t)
 elif x=='k':
  for d in K8:
   t=s+d
   if 0<=t<64 and abs(t%8-f)<=1 and abs(t//8-r)<=1:put(t)
  if w and s==4 or not w and s==60:
   for t,u,need in ((s+2,s+3,'K'if w else'k'),(s-2,s-4,'Q'if w else'q')):
    if need in rights and b.get(u)==('R'if w else'r') and all(i not in b for i in range(min(s,t)+1,max(s,t))):o.append((t,''))
 elif x in D:
  for d in D[x]:
   t=s
   while 1:
    z=t;t+=d
    if not 0<=t<64 or (abs(t%8-z%8)>1 and t//8!=z//8):break
    if t in b:
     if b[t].isupper()!=w:o.append((t,''))
     break
    o.append((t,''))
 elif x=='p':
  d=8 if w else-8;st=1 if w else 6;t=s+d
  if 0<=t<64 and t not in b:
   o.extend((t,z)for z in'qrbn')if t//8 in(0,7)else o.append((t,''))
   if r==st and s+2*d not in b:o.append((s+2*d,''))
  for d in (d-1,d+1):
   t=s+d
   if 0<=t<64 and abs(t%8-f)==1 and ((t in b and b[t].isupper()!=w) or t==ep):
    o.extend((t,z)for z in'qrbn')if t//8 in(0,7)else o.append((t,''))
 return o
def attacked(b,t,w):
 return any(t in (z for z,_ in moves(b,s,None)) for s,p in b.items() if p.isupper()==w)
def king(b,w):return next((s for s,p in b.items() if p==('K'if w else'k')),None)
def play(b,s,t,pr,cas,ep):
 b=dict(b);x=b.pop(s);w=x.isupper();lo=x.lower()
 if lo=='p' and t==ep and t not in b and abs(t%8-s%8)==1:b.pop(t-(8 if w else-8),None)
 b[t]=(pr.upper()if w else pr)if pr else x
 if lo=='k' and abs(t-s)==2:
  r=(0 if w else 7)*8;u=r+(7 if t>s else 0);v=r+(5 if t>s else 3)
  if u in b:b[v]=b.pop(u)
 n=cas
 if lo=='k':n=n.replace('K'if w else'k','').replace('Q'if w else'q','')
 for ch,f in (('K',7),('Q',0),('k',63),('q',56)):
  if t==f:n=n.replace(ch,'')
 n=n or'-';ne=(s+t)//2 if lo=='p' and abs(t-s)==16 else None
 return b,n,ne
def legal(b,s,cas,ep):
 global rights
 rights=cas
 for a,p in list(b.items()):
  if p.isupper()!= (s=='w'):continue
  for t,pr in moves(b,a,ep):
   z,n,e=play(b,a,t,pr,cas,ep);k=king(z,s=='w')
   if k is not None and not attacked(z,k,s!='w'):yield a,t,pr,z,n,e
def val(b):return sum(V[p.lower()]*(1 if p.isupper() else-1) for p in b.values())
def search(b,s,cas,ep,d,lo=-10**9,hi=10**9):
 if not d:return val(b)*(1 if s=='w' else-1)
 a=list(legal(b,s,cas,ep))
 if not a:return -999999
 best=-10**9
 for x,y,p,z,c,e in a:
  q=-search(z,'b'if s=='w'else'w',c,e,d-1,-hi,-lo);best=max(best,q);lo=max(lo,q)
  if lo>=hi:break
 return best
def choose(fen,allowed):
 b,s,cas,ep=pos(fen);w=s=='w';m={}
 for a,t,p,z,c,e in legal(b,s,cas,ep):
  u=chr(a%8+97)+str(a//8+1)+chr(t%8+97)+str(t//8+1)+(p or '')
  if u in allowed:m[u]=-search(z,'b'if w else'w',c,e,1)
 return max(allowed,key=lambda x:(m.get(x,-10**9),-allowed.index(x)))
def post(url,path,body):
 q=urllib.request.Request(url+path,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
 with urllib.request.urlopen(q) as r:return json.load(r)
def run():
 url=os.environ.get('MAKEFUN_ENV_URL')
 if not url:return
 g=post(url,'/game',{})
 while g.get('status')!='done':
  if g.get('status')=='your_move':g=post(url,'/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
  else:g=post(url,'/game',{})
if __name__=='__main__':
 if os.environ.get('MAKEFUN_ENV_URL'):run()
 else:
  for line in sys.stdin:
   try:
    q=json.loads(line);print(choose(q['fen'],q['legal_moves']),flush=True)
   except Exception:print('',flush=True)
