# api_tester_app.py
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    # Serve a single HTML page with embedded JavaScript and CSS
    return render_template('tester.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)