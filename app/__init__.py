from flask import Flask
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 10000

app.wsgi_app = SassMiddleware(
    app.wsgi_app,
    {
        'app': {
            'sass_path': 'static/sass',
            'css_path': 'static/css',
            'wsgi_path': '/static/css',
            'strip_extension': False
        }
    }
)


from app import routes
