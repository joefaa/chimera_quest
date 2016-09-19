import jinja2
from chimera_quest.model import chimera_quest
import cgi
import sys
from tempfile import TemporaryFile
import os
def application( environ, start_response ):

    templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
    env = jinja2.Environment( loader=templateLoader )
    template = env.get_template( 'main.html' )

    tissue_type = None
    input_type = None
    input_file = None
    user_input = []

    if environ['REQUEST_METHOD'] == 'POST':

        Q_S = cgi.parse_qs(environ['QUERY_STRING'])
        input_type = Q_S.get('input_type', [''])[0]
        tissue_type = Q_S.get('tissue_type', [''])[0]

        length = int(environ.get('CONTENT_LENGTH', 0))
        stream = environ['wsgi.input']
        body = TemporaryFile(mode='w+b')
        while length > 0:
            part = stream.read(min(length, 1024*200)) # 200KB buffer size
            if not part: break
            body.write(part)
            length -= len(part)
        body.seek(0)
        environ['wsgi.input'] = body
        form = cgi.FieldStorage(fp=body, environ=environ, keep_blank_values=True)

        input_file = form['input_file'].file.read().decode("utf-8")

        user_input = [tissue_type, input_type, input_file]

    if input_type:

        fusion_list = chimera_quest( user_input )
        start_response("200 OK", [( "Content-Type", "text/html" )], ('Content-Length', str(len(fusion_list))))
        yield(fusion_list.encode( "utf8" ))

    else:
        template = template.render()
        start_response("200 OK", [( "Content-Type", "text/html" ),  ('Content-Length', str(len(template)))])
        yield(template.encode( "utf8" ))
