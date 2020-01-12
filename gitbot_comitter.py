import http.server, re, os, subprocess, urllib.parse

# This file is run by the gitbot on the server (seperately) to listen for requests specifying git commits that should be done.

class PostHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['content-length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        mo = queryRE.search(post_data)
        filepath = mo.group(1)
        commitmsg = mo.group(2)
        filepath = urllib.parse.unquote_plus(filepath)
        commitmsg = urllib.parse.unquote_plus(commitmsg)
        filepath = os.path.abspath(filepath)
        directory = os.path.dirname(filepath)
        if not directory.startswith(os.getcwd()) or directory.endswith(os.getcwd()):
            self.send_response(403)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'You don\'t have permission to complete this operation.' + filepath.encode('utf-8'))
        else:
            process_one = subprocess.run(['git', 'add', filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if not process_one.returncode:
                process_two = subprocess.run(['git', 'commit', '-m', commitmsg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if process_one.returncode or process_two.returncode:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid request.\n' + process_one.stdout + process_two.stdout)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(process_one.stdout + process_two.stdout)

queryRE = re.compile(r'filepath=(.*)&commitmsg=(.*)')

server = http.server.HTTPServer(server_address=('127.0.0.1', 6553), RequestHandlerClass=PostHandler)
server.serve_forever()