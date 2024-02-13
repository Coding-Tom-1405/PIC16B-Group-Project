from flask import Flask, render_template, request
from flask import redirect, url_for, abort

app = Flask(__name__)

@app.route("/") # decorators
def hello_world():
    return "<h1>Hello, World!</h1>"
