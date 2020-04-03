import os
from os import path
import json
import random
from datetime import datetime, date, time
from jinja2 import Environment, FileSystemLoader
import uuid
from flask import jsonify

task_folder = "./backend/tasks"
task_count = 3
task_ids = []

def init_ids():
    task_ids = []
    for dir in range(task_count):
        ids = []
        for file in os.listdir(path.join(task_folder, str(dir))) :
           with open(path.join(task_folder, str(dir), file)) as fd:
               ids.append(json.load(fd)['id'])
        task_ids.append(ids)
    return task_ids
                     
def fill_correct_ids():
    for dir in range(task_count):
        for file in os.listdir(path.join(task_folder, str(dir))) :
            with open(path.join(task_folder, str(dir), file), 'r') as fd:
               data = json.load(fd)
               id = generate_id_for_task_number(dir)
               data['id'] = str(id)
               file_name = F"task{id}.json"
               with open(path.join(task_folder, str(dir), file_name), 'w') as f:
                    json.dump(data, f)
            os.remove(path.join(task_folder, str(dir), file))

def generate_id_for_task_number(num):
    if num >= task_count:
        raise ValueError("num must be less then tasks count")
    while True:
        id = uuid.uuid4()
        if (get_task_number_by_(id) == num):
            return id
        
def hash_id(id, max):
    res = 0
    for ch in str(id):
        res = res ^ ord(ch)
    return res % max

def get_task_number_by_(id):
    return hash_id(id, task_count)

def get_next_task_id_by_(next_task_num):
    task_ids = init_ids()
    ids = task_ids[next_task_num]
    ind = random.randint(0, len(ids) - 1)
    return ids[ind]
                     
def its_time():
    dateZ = date(5, 4, 2020)
    timeFrom = time(15, 0, 0)
    timeTo = time(23, 59, 59)
                               
    dtFrom = datatime(date, timeFrom)
    dtTo = datatime(date, timeTo)
                               
    dt = datetime.now()
    return dt > dtFrom and dt < dtTo
        

def get_index():
    env = Environment(loader=FileSystemLoader('frontend'))
    template = env.get_template('index.html')
    html_content = template.render()
    return html_content

def fetch_task (id):
    # get file
    if id == 'super':
        return fetch_super_task()
        
    num = get_task_number_by_(id)
    file_name = F"{num}/task{id}.json"
    file_path = path.join(task_folder, file_name)
    print("api >> fetch_task", file_path)
    if not path.exists(file_path):
        return None
    # get task
    with open(file_path) as fd:
        task = json.load(fd)
    return task

def fetch_super_task():
    file_name = F"super/task.json"
    file_path = path.join(task_folder, file_name)
    print("api >> fetch_super_task", file_path)
    if not path.exists(file_path):
        return None
    # get task
    if its_time():
        with open(file_path) as fd:
            task = json.load(fd)
        return task
    else:
        return jsonify()

# id - string
def post_task (id):
    if id == 'undefined' or id == '' :
        id = get_next_task_id_by_(0)
        print("api >> post_task", id)
    task_json = fetch_task(id)
    if task_json:
        return json.dumps(id=task_json["id"], text=task_json["text"], type=task_json["type"])
    return jsonify()

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

# Может разделить? Проверка правильности ответа и отправка нового задания
def post_solution (id, solution):
    task_json = fetch_task(id)
    if task_json:
        print("api >> post_solution", solution)
        print("api >> post_solution", task_json["solution"])
        if ordered(task_json["solution"]) == ordered(solution):
            next_task_num = get_task_number_by_(id) + 1
            if next_task_num >= task_count:
                return jsonify(success="true")
            next_id = get_next_task_id_by_(next_task_num)
            print("api >> post_solution", next_id, " ", next_task_num)
            return jsonify(success="true", next_task=post_task(next_id))
        return jsonify(success="false")
    return jsonify()

if __name__ == "__main__" :
    task_ids = init_ids()
    #fill_correct_ids()
    print(task_count)
    print(post_task('0'))
    print(post_task(''))
    print()
    print(post_solution(0, "4"))
    print(post_solution(0, "5"))


# TODO:
# 1. Выбор рандомного задания. Проблема: нужно где-то хранить пройденные задания.
# 2. id - число. а не uuid4
# 3. ...
