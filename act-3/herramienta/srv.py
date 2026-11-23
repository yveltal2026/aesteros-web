import http.server,os,sys
D=sys.argv[1]; P=int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=D,**k)
    def do_GET(s):
        p=s.path.split('?')[0]
        if '.' not in os.path.basename(p) and not p.startswith('/_'): s.path='/index.html'
        return super().do_GET()
    def log_message(s,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',P),H).serve_forever()
