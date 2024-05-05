from flask import Flask, request, redirect,abort
import random
import string
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://urlsshorten.netlify.app"}})
client = MongoClient('mongodb+srv://yashtyagis2016:9qHwOvw6W9cJzc9T@cluster0.lsfl3tw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['url_shortener']
urls_collection = db['urls']

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return 'Welcome to URL Shortener!'

@app.route('/check_connection')
def check_connection():
    try:
        client.admin.command('ismaster')  # Attempt a simple operation to check the connection
        return 'Connection to MongoDB successful!'
    except Exception as e:
        return f'Connection to MongoDB failed: {e}', 500

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')
    short_code = generate_short_code()
    urls_collection.insert_one({'long_url': long_url, 'short_code': short_code})
    short_url = request.host_url + short_code
    return {'shorten':short_url}

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    result = urls_collection.find_one({'short_code': short_code})
    if result:
        long_url = result['long_url']
        return redirect("https://"+long_url)
    else:
        return 'Short URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
