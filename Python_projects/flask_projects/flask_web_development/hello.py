#!/usr/bin/python
# -*- coding: UTF-8 *-*

from flask import Flask,jsonify
from flask import redirect

app = Flask(__name__)

@app.route('/')
def index():
    #return '<h1>Hello World!</h1>'
    return redirect('http://www.example.com')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s\n!</h1>' %name

if __name__ == '__main__':
    app.run(debug=True)
