from jinja2 import Environment, FileSystemLoader
from flask import Flask
from flask import request
import backend.api as api
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def get_index():
    return api.get_index()

@app.route('/api/task/get', methods=['POST'])
def post_task_get():
    if not request.json or not 'id' in request.json:
        abort(400)
    return api.post_task(request.json['id'])

@app.route('/api/task/solve', methods=['POST'])
def post_task_solve():
    if not request.json or not 'id' in request.json:
        abort(400)
    return api.post_solution(request.json['id'], request.json['solution'])

if __name__ == '__main__':
    app.run()