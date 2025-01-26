#Simplest app.py code for demo
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "<img src=https://cataas.com/cat>"
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
