# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from views import *

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)