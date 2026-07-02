from livereload import Server
import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
DOCS = os.path.join(ROOT, 'docs')

server = Server()
# Watch docs and static assets
server.watch(DOCS)
server.watch(os.path.join(ROOT, 'css'))
server.watch(os.path.join(ROOT, 'js'))

print('Serving site with livereload at http://localhost:8000')
server.serve(root=ROOT, host='0.0.0.0', port=8000, open_url_delay=None)