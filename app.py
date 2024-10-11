from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    test_suites = db.relationship('TestSuite', backref='project', lazy=True)

class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='not_run')  # Default to 'not_run'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# Function to create the tables if they don't exist
def create_tables():
    with app.app_context():
        db.create_all()

# Route to get the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API route to add a project
@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    project_name = data.get('name')
    test_suites = data.get('test_suites')

    # Create a new project
    new_project = Project(name=project_name)
    db.session.add(new_project)
    db.session.flush()

    # Create test suites
    for suite_name in test_suites:
        new_suite = TestSuite(name=suite_name, project_id=new_project.id)
        db.session.add(new_suite)

    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

# API route to get all projects and their test suites
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    project_data = []
    for project in projects:
        project_data.append({
            'id': project.id,
            'name': project.name,
            'test_suites': [{'id': ts.id, 'name': ts.name, 'status': ts.status} for ts in project.test_suites]
        })
    return jsonify(project_data)

# API route to update test suite status
@app.route('/api/test-suite/<int:test_suite_id>', methods=['PATCH'])
def update_test_suite_status(test_suite_id):
    data = request.json
    new_status = data.get('status')
    
    test_suite = TestSuite.query.get(test_suite_id)
    if not test_suite:
        return jsonify({'message': 'Test suite not found'}), 404

    test_suite.status = new_status
    db.session.commit()

    return jsonify({'message': 'Status updated successfully'})

if __name__ == '__main__':
    # Ensure tables are created when the application starts
    create_tables()
    app.run(host='0.0.0.0', debug=True)
