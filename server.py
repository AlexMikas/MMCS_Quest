from jinja2 import Environment, FileSystemLoader
from flask import Flask
from flask import request
import backend.api as api
app = Flask(__name__, static_folder='frontend/static')

@app.route('/')
@app.route('/index.html')
@app.route('/tasks.html')
@app.route('/supertask.html')
def get_index():
    return api.get_index()

@app.route('/api/task/get', methods=['POST'])
def post_task_get():
    if not request.json or not 'id' in request.json:
        abort(400)
    print("server >> post_task_get", request.json)
    return api.post_task(request.json['id'])

@app.route('/api/task/solve', methods=['POST'])
def post_task_solve():
    if not request.json or not 'id' in request.json:
        abort(400)
    print("server >> post_task_solve", request.json)
    meow = api.post_solution(request.json['id'], request.json['solution'])
    print("server >> post_task_solve", meow)
    return meow

if __name__ == '__main__':
    app.run()
