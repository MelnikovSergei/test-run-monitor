from flask import Flask, render_template, request, jsonify
from utils.project import Project
app = Flask(__name__)
project = Project()
project.name = "test"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    data = request.get_json()
    project_name = data['project_name']
    project.add_test_suite(project_name)
    print(project.test_suites)
    # Add project to database or perform other tasks
    return jsonify({'message': f'Project {project_name} has been added successfully!'})

@app.route('/check-status', methods=['POST'])
def check_status():
    print(request.get_json()['suiteName'])
    suite_name = request.get_json()['suiteName']
    # Your logic to get the status of the test suite goes here
    
    status = project.get_suite_status(suite_name)
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run()
