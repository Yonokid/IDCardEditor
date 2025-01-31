from flask import Flask
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 10000

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/sass', 'static/css', '/static/css')
})

from app import routes
