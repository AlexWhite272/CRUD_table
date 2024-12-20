from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS

import database

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

@app.route('/api/teacher/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    if type(teacher_id) != int:
        abort(400)

    result = database.select_teacher(teacher_id)
   
    return create_response(result)

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    result = database.select_teacher()

    return create_response(result)

@app.route('/api/students', methods=['GET'])
def get_students():
    result = database.select_students()
    
    return create_response(result)

@app.route('/api/student/<int:student_id>', methods=['GET'])
def get_student(student_id):

    if type(student_id) != int:
        abort(400)

    result = database.select_students(student_id)
    
    return create_response(result)

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    result = database.select_subjects()
    
    return create_response(result)

@app.route('/api/genders', methods=['GET'])
def get_genders():
    result = database.select_genders()
    
    return create_response(result)

@app.route('/api/workloads', methods=['GET'])
def get_workloads():
    result = database.select_workloads()
    
    return create_response(result)

@app.route('/api/classes', methods=['GET'])
def get_classes():
    result = database.select_classes()
    
    return create_response(result)


@app.route('/api/students', methods=['POST'])
def create_students():
    
    if not request.json:
        abort(400)

    result = database.add_students(request.json)

    return create_response(result)

@app.route('/api/teachers', methods=['POST'])
def create_teachers():
    
    if not request.json:
        abort(400)

    result = database.add_teachers(request.json)

    return create_response(result)



@app.route('/api/update/teachers', methods=['PUT', 'POST'])
def update_teacher():
    if not request.json:
        abort(400)

    if "id" not in request.json:
        abort(400)

    result = database.update_teachers(request.json)

    return create_response(result)

@app.route('/api/update/students', methods=['PUT', 'POST'])
def update_student():
    if not request.json:
        abort(400)

    if "id" not in request.json:
        abort(400)

    result = database.update_teachers(request.json)

    return create_response(result)



@app.route('/api/delete/student/<int:student_id>', methods=['DELETE', 'GET'])
def delete_student(student_id):
    
    if type(student_id) != int:
        abort(400)

    result = database.delete_students(student_id)

    return create_response(result)

@app.route('/api/delete/student/<int:teacher_id>', methods=['DELETE', 'GET'])
def delete_teacher(teacher_id):
    
    if type(teacher_id) != int:
        abort(400)

    result = database.delete_teacher(teacher_id)

    return create_response(result)



@app.errorhandler(400)
def bad_request(error):
    result = database.create_data_answer(400, "Bad request!")
    return create_response(result)

@app.errorhandler(404)
def not_found(error):
    result = database.create_data_answer(404, "Not found!")
    return create_response(result)

@app.errorhandler(500)
def server_error(error):
    result = database.create_data_answer(500, "Сервер обнаружил внутреннюю ошибку и не смог выполнить ваш запрос. Либо сервер перегружен, либо в приложении произошла ошибка.")
    return create_response(result)

def create_response(result):
    response = make_response(jsonify(result), result.get('code'))
    response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(port=5000)
   

