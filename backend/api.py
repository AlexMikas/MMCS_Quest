import os
from os import path
import json
import random
from datetime import datetime, date, time
from jinja2 import Environment, FileSystemLoader
import uuid

task_folder = "./backend/tasks"
task_count = 3
task_ids = []

def init_ids():
    task_ids = []
    for dir in range(task_count):
        ids = []
        for file in os.listdir(path.join(task_folder, str(dir))) :
           with open(path.join(task_folder, str(dir), file), encoding="utf-8") as fd:
               ids.append(json.load(fd)['id'])
        task_ids.append(ids)
    return task_ids
                     
def fill_correct_ids():
    for dir in range(task_count):
        for file in os.listdir(path.join(task_folder, str(dir))) :
            with open(path.join(task_folder, str(dir), file), encoding="utf-8") as fd:
               data = json.load(fd)
               id = generate_id_for_task_number(dir)
               data['id'] = str(id)
               file_name = F"task{id}.json"
               with open(path.join(task_folder, str(dir), file_name), 'w', encoding="utf-8") as f:
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
    dateZ = date(2020, 4, 3)
    timeFrom = time(14, 0, 0)
    timeTo = time(23, 59, 59)
                               
    dtFrom = datetime.combine(dateZ, timeFrom)
    dtTo = datetime.combine(dateZ, timeTo)
                               
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
    with open(file_path, encoding="utf-8") as fd:
        task = json.load(fd)
    return task

def fetch_super_task():
    file_name = F"super/task.json"
    file_path = path.join(task_folder, file_name)
    print("api >> fetch_super_task", file_path)
    if not path.exists(file_path):
        return None
    # get task
    with open(file_path, encoding="utf-8") as fd:
        task = json.load(fd)
    if its_time():
        return task
    else:
        task["text"] = "Задача станет доступна после 05.04.2020г. 14:00 по мск!"
        return task

# id - string
def post_task (id):
    if id == 'undefined' or id == '' :
        id = get_next_task_id_by_(0)
        print("api >> post_task", id)
    task_json = fetch_task(id)
    if task_json:
        desc_json = {"id": task_json["id"], "text": task_json["text"], "type": task_json["type"]}
        return json.dumps(desc_json)
    return "{}"


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
        res = {"success": False, "next_id": None}
        if task_json["type"] == "equations":
            for solu in task_json["solution"]:
                if ordered(solu) == ordered(solution):
                    next_task_num = get_task_number_by_(id) + 1
                    res["success"] = True
                    if next_task_num >= task_count:
                        return json.dumps(res)
                    next_id = get_next_task_id_by_(next_task_num)
                    print("api >> post_solution", next_id, " ", next_task_num)
                    res["next_task"] = json.loads(post_task(next_id))
                    break
        else:
            next_task_num = get_task_number_by_(id) + 1
            res["success"] = True
            if next_task_num >= task_count:
                return json.dumps(res)
            next_id = get_next_task_id_by_(next_task_num)
            print("api >> post_solution", next_id, " ", next_task_num)
            res["next_task"] = json.loads(post_task(next_id))
        return json.dumps(res)
    return "{}"

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
