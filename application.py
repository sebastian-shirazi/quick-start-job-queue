from flask import Flask, request, jsonify, Response
from project.main import Queue


app = Flask(__name__)
q = Queue()

@app.route('/')
def print_welcome():
    return Response(jsonify({'Read from file': 'use curl http://localhost:5000/file_name to get started', 'Get first job in Queue': 'use curl http://localhost:5000/jobs', 'Add job to Queue': 'use curl -X POST http://localhost:5000/jobs -H "Content-Type: application/json" -d "{"uuid": "ex_uuid", "priority": "ex_priority (num)", "name": "ex_name"}"', 'Get job by number': 'use curl http://localhost:5000/jobs/job_num', 'Get all jobs': 'use curl http://localhost:5000/jobs/status', 'Delete job by uuid': 'use curl -X DELETE http://localhost:5000/jobs/uuid', 'Delete first job in Queue': 'use curl -X DELETE http://localhost:5000/jobs', 'Change order of queue (alread initialized)': 'use curl http://localhost:5000/sorting_method/jobs', 'Delete all jobs': 'use curl -X DELETE http://localhost:5000/jobs/all'}), status=200)

@app.route('/<file_name>' , methods=['GET'])
def initialize_queue(file_name):
    if 'txt' not in file_name:
        return Response(jsonify({'Error': 'Invalid file format - file not found or not a .txt file'}), status=404)
    try:
        q.clear_queue()
        q.read_file(file_name)
        q.sort_method = 'priority'
        q.custom_sort()
        return Response(jsonify({'Success': 'Queue initialized'}), status=200)
    except FileNotFoundError:
        return Response(jsonify({'Error': 'File not found'}), status=404)

@app.route('/<sorting_method>/jobs' , methods=['GET'])
def modify_queue_with_specified_sort(sorting_method):
    sorting_method = sorting_method.lower()
    if not q.is_empty():
        if sorting_method not in ["fifo", "lifo", "priority"]:
            return Response(jsonify({'Error': 'Invalid sort method'}), status=400)
        q.sort_method = sorting_method
        q.custom_sort()
        return Response(jsonify({'Success': 'Queue resorted by ' + sorting_method}), status=200)
    return Response(jsonify({'Error': 'Queue is empty'}), status=400)

@app.route('/jobs', methods=['GET', 'POST', 'DELETE'])
def get_or_add_job():
    if request.method == 'GET':
        if q.is_empty():
            return Response(jsonify({'Error': 'Queue is empty'}), status=400)
        job = q.peek()
        if job:
            return Response(jsonify({'uuid:': job[0], 'name': job[1], 'priority': job[2], 'exec_time': job[3]}), status=200)
    if request.method == 'POST':
        data = request.json
        if "priority" and "exec_time" not in data:
            q.enqueue(data.get("uuid"), data.get("name"), q.DEFAULT_PRIORITY, q.DEFAULT_TIME, q.size()+1)
        elif "priority" not in data:
            q.enqueue(data.get("uuid"), data.get("name"), q.DEFAULT_PRIORITY, int(data.get("exec_time")), q.size()+1)
        elif "exec_time" not in data:
            q.enqueue(data.get("uuid"), data.get("name"), int(data.get("priority")), q.DEFAULT_TIME, q.size()+1)
        elif not data.get("priority").isdigit() or not data.get("exec_time").isdigit():
            return Response(jsonify({'Error': 'Invalid priority / exec_time - must be an integer'}), status=400)
        else:
            q.enqueue(data.get("uuid"), data.get("name"), q.size()+1, int(data.get("priority")), int(data.get("exec_time")))
        q.custom_sort()
        return Response(jsonify({"Success": "Job added to queue", "uuid": data.get("uuid"), "name": data.get("name"), "priority": data.get("priority", "10"), "exec_time": data.get("exec_time", "0")}), status=200)
    if request.method == 'DELETE':
        if q.is_empty():
            return Response(jsonify({'Error': 'Queue is empty'}), status=400)
        removed_job = q.dequeue()
        return Response(jsonify({'Success': 'Job Removed', 'uuid:': removed_job[0], 'name': removed_job[1], 'priority': removed_job[2], 'exec_time': removed_job[3]}), status=200)

@app.route('/jobs/<job_num>', methods=['GET'])
def get_job_by_num(job_num):
    if q.is_empty():
        return Response(jsonify({'Error': 'Queue is empty'}), status=400)
    if not job_num.isdigit() or int(job_num) > q.size() or int(job_num) < 1:
        return Response(jsonify({'Error': 'Invalid job number'}), status=400)
    job = q.queue[int(job_num)-1]
    return Response(jsonify({'uuid:': job[0], 'name': job[1], 'priority': job[2], 'exec_time': job[3]}), status=200)

@app.route('/jobs/status', methods=['GET'])
def get_status():
    json_array = []
    if q.is_empty():
        return Response(jsonify({'Error': 'Queue is empty'}), status=400)
    for job in q.queue:
        json_array.append({'uuid': job[0], 'name': job[1], 'priority': job[2], 'exec_time': job[3]})
    return Response(json_array, status=200)

@app.route('/jobs/run', methods=['GET'])
def run_job():
    if q.is_empty():
        return Response(jsonify({'Error': 'Queue is empty'}), status=400)
    removed_job = q.run_task()
    return Response(jsonify({'Success': 'Job Completed', 'uuid:': removed_job[0], 'name': removed_job[1], 'priority': removed_job[2]}), status=200)

@app.route('/jobs/<uuid>', methods=['DELETE'])
def delete_job(uuid):
    if q.is_empty():
        return Response(jsonify({'Error': 'Queue is empty'}), status=400)
    for job in q.queue:
        if job[0] == str(uuid):
            removed_job = q.dequeue()
            return Response(jsonify({'Success': 'Job Removed', 'uuid:': removed_job[0], 'name': removed_job[1], 'priority': removed_job[2]}), status=200)
    return Response(jsonify({'Error': 'Job not found in queue'}), status=400)

@app.route('/jobs/all', methods=['DELETE'])
def delete_all_jobs():
    if q.is_empty():
        return Response(jsonify({'Error': 'Queue is empty'}), status=400)
    q.clear_queue()
    return Response(jsonify({'Success': 'All jobs removed'}), status=200)


if __name__ == '__main__':
    app.run(debug=True)
