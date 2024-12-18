from flask import Flask

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 10000

from app import routes
