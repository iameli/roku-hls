from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi
import streamlink
import urllib
import requests

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        # if ctype != 'application/json':
        #     self.send_response(400)
        #     self.end_headers()
        #     return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))

        streams = streamlink.streams(message['url'])
        stream = streams["best"]
        print(stream.url)

        query = urllib.urlencode({
            "live": "true",
            "autoCookie": "false",
            "debugVideoHud": "false",
            "url": stream.url,
            "fmt": "auto",
            "drmParams": '{}',
            "headers": '{}',
            "metadata": '{"isFullHD":false}',
            "cookies": '{}',
        })
        
        req = "http://10.9.168.122:8060/launch/63218?%s" % query
        r = requests.post(url = req) 
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print 'Starting httpd on port %d...' % port
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        