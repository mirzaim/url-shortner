from pymongo import MongoClient
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, abort
from string import digits, ascii_letters
from secrets import choice
import time

max_redirect_len = 7
alphabet = digits + ascii_letters
mongo_client = MongoClient('db',
                            username=getenv('MONGO_INITDB_ROOT_USERNAME'),
                            password=getenv('MONGO_INITDB_ROOT_PASSWORD'))
db = mongo_client[getenv('MONGO_INITDB_DATABSE')]
redirects = db.redirects
EXP_DUR = int(getenv('APP_EPIRATION_TIME'))
PORT_NUM = int(getenv('APP_PORT_NUM'))

app = Flask(__name__, template_folder='/app/templates/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>', methods=['GET'])
def path_redirect(path):
    global redirects

    redirect_path = redirects.find_one({'path_from': path})

    if not redirect_path:
        return render_template('404.html')
    elif redirect_path['insertion_time'] + EXP_DUR < int(time.time()):
        return render_template('expirated.html')
    else:
        return render_template('redirect.html', redirect_path=redirect_path['path_to'])

@app.route('/shortit', methods=['POST'])
def register_path():
    global max_redirect_len
    global redirects
    global redirect_admin_pwd

    json_data = request.get_json()
    admin_pwd, path_from, path_to = None, None, None

    try:
        path_to = json_data['path_to']
    except:
        abort(500, description='Invalid parameters provided')
    

    if path_to[:7] != 'http://' and path_to[:8] != 'https://':
        abort(400, description='Invalid URL scheme provided')

    
    existing_redirect = redirects.find_one({'path_to':path_to})

    if existing_redirect:
        redirects.find_one_and_delete(existing_redirect)
        # redirects.find_one_and_update(existing_redirect, {'path_from': existing_redirect["path_from"],
        #                                                   'path_to': existing_redirect["path_to"], 'insertion_time': int(time.time())})
        return f'URL for {path_to} already exists at {existing_redirect["path_from"]}. We extended expiration time.'
    else:
        path_from = ''.join([choice(alphabet) for i in range(max_redirect_len)])
        
        while redirects.find_one({'path_from':path_from}):
            path_from = ''.join([choice(alphabet) for i in range(max_redirect_len)])

        redirects.insert_one({'path_from':path_from, 'path_to':path_to, 'insertion_time': int(time.time())})

    return f'URL created for {path_to} at /{path_from}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT_NUM)