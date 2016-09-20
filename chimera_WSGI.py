from wsgiref.simple_server import make_server
from chimera_quest.view import application
from whitenoise import WhiteNoise

application = WhiteNoise(application, root='./static')

httpd = make_server('localhost', 8051, application)
httpd.serve_forever()
