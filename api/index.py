from flask import Flask
from random import randint

app = Flask(__name__)

@app.route('/')
def home():
    return f'Hello, World!\nCoin: {["Heads","Tails"][randint(0,1)]}'

@app.route('/about')
def about():
    return 'About'
