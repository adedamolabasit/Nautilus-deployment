from flask import Flask ,render_template
import requests





app=Flask(__name__,template_folder='templates')

@app.route('/')
def home():
    proxies = {
    "https":'https://154.16.202.22:3128',
    "http":'http://154.16.202.22:3128'
    }
    response=requests.get('http://127.0.0.1:5000/users',proxies=proxies)
    print(response)
    return render_template('nautilus/index.html')