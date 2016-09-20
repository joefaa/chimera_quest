from chimera_quest.view import application
from whitenoise import WhiteNoise

application = WhiteNoise(application, root='./static')
