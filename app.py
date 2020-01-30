#!/usr/bin/env python3
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

diaries = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

user = [
    {
        'id': 1,
        'username': u'victor',
        'password': u'python'
    }
]


@app.route('/todo/api/v1.0/diaries/<int:diary_id>', methods=['GET'])
def get_diary(diary_id):
    diary = [diary for diary in diaries if diary['id'] == diary_id]
    if len(diary) == 0:
        abort(404)
    return jsonify({'diary': diary[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/diaries', methods=['POST'])
def create_diary():
    if not request.json or not 'title' in request.json:
        abort(400)
    diary = {
        'id': diaries[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }

    for i in diaries:
        if i['title'] != diary['title'] and i['description'] != diary['description']:
            diaries.append(diary)
            return jsonify({'diary': diary}), 201
        else:
            return make_response(jsonify({'error': 'Cannot do so please change title and description.'}), 403)


@app.route('/todo/api/v1.0/diaries/<int:diary_id>', methods=['PUT'])
def update_diary(diary_id):
    diary = [diary for diary in diaries if diary['id'] == diary_id]
    if len(diary) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    diary[0]['title'] = request.json.get('title', diary[0]['title'])
    diary[0]['description'] = request.json.get(
        'description', diary[0]['description'])
    diary[0]['done'] = request.json.get('done', diary[0]['done'])
    return jsonify({'diary': diary[0]})


@app.route('/todo/api/v1.0/diaries/<int:diary_id>', methods=['DELETE'])
def delete_diary(diary_id):
    diary = [diary for diary in diaries if diary['id'] == diary_id]
    if len(diary) == 0:
        abort(404)
    diaries.remove(diary[0])
    return jsonify({'result': True})


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/todo/api/v1.0/diaries', methods=['GET'])
def get_diaries():
    return jsonify({'diaries': [make_public_diary(diary) for diary in diaries]})


def make_public_diary(diary):
    new_diary = {}
    for field in diary:
        if field == 'id':
            new_diary['uri'] = url_for(
                'get_diary', diary_id=diary['id'], _external=True)
        else:
            new_diary[field] = diary[field]
    return new_diary


@auth.get_password
def get_password(username):
    if username == 'victor':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(debug=True)
