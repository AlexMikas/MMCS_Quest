import os
from os import path
import json
import random
task_folder = "./tasks"
task_count = 0

def init ():
    task_count = 0
    for file in os.listdir(task_folder):
        task_count += 1
    return task_count

def fetch_task (id):
    # get file
    file_name = "task"+str(id)+".json"
    file_path = path.join(task_folder, file_name)
    if not path.exists(file_path):
        return None
    # get task
    task = json.load(open(file_path))
    return task

# id - string
def post_task (id):
    if id == '':
        id = random.randint(0, task_count - 1)
    task_json = fetch_task(id)
    if task_json:
        desc_json = {"id": task_json["id"], "text": task_json["text"], "type": task_json["type"]}
        return json.dumps(desc_json)
    return "{}"

# Может разделить? Проверка правильности ответа и отправка нового задания
def post_solution (id, solution):
    task_json = fetch_task(id)
    if task_json:
        if task_json["solution"] == solution:
            next_id = id + 1
            return '{"success": true, next_task: '+ post_task(next_id) +'}'
        return '{"success": false}'
    return "{}"

if __name__ == "__main__" :
    task_count = init()
    print(task_count)
    print(post_task('0'))
    print(post_task(''))
    print()
    print(post_solution(0, "4"))
    print(post_solution(0, "5"))



