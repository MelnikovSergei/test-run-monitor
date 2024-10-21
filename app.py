from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'test_suites': [suite.to_dict() for suite in self.test_suites]
        }

class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='not_run')  # Default to 'not_run'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'project_id': self.project_id
        }

# Function to create the tables if they don't exist
def create_tables():
    with app.app_context():
        db.create_all()

# Route to get the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API route to get all projects and their test suites
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

# API route to get a specific project by ID
@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())

# API route to add a project
@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    project_name = data.get('name')
    test_suites = data.get('test_suites', [])

    # Create a new project
    new_project = Project(name=project_name)
    db.session.add(new_project)
    db.session.flush()

    # Create test suites if any are provided
    for suite_name in test_suites:
        new_suite = TestSuite(name=suite_name, project_id=new_project.id)
        db.session.add(new_suite)

    db.session.commit()
    return jsonify(new_project.to_dict()), 201

# API route to update a project by ID
@app.route('/api/projects/<int:project_id>', methods=['PATCH'])
def update_project(project_id):
    data = request.json
    new_name = data.get('name')

    project = Project.query.get_or_404(project_id)
    project.name = new_name
    db.session.commit()

    return jsonify({'message': 'Project updated successfully'})

# API route to delete a project by ID
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404

    # Delete associated test suites
    TestSuite.query.filter_by(project_id=project_id).delete()

    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted successfully'})

# API route to add a test suite to a project
@app.route('/api/projects/<int:project_id>/test-suite', methods=['POST'])
def add_test_suite(project_id):
    data = request.json
    test_suite_name = data.get('name')

    project = Project.query.get_or_404(project_id)

    # Create a new test suite and associate it with the project
    new_test_suite = TestSuite(name=test_suite_name, project_id=project.id)
    db.session.add(new_test_suite)
    db.session.commit()

    return jsonify(new_test_suite.to_dict()), 201

# API route to update a test suite status
@app.route('/api/test-suite/<int:test_suite_id>', methods=['PATCH'])
def update_test_suite(test_suite_id):
    test_suite = TestSuite.query.get_or_404(test_suite_id)
    data = request.json
    new_status = data.get('status')

    test_suite.status = new_status
    db.session.commit()

    return jsonify(test_suite.to_dict())

# API route to delete a test suite
@app.route('/api/test-suite/<int:test_suite_id>', methods=['DELETE'])
def delete_test_suite(test_suite_id):
    test_suite = TestSuite.query.get_or_404(test_suite_id)

    db.session.delete(test_suite)
    db.session.commit()

    return '', 204

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return a 200 OK response

if __name__ == '__main__':
    # Ensure tables are created when the application starts
    create_tables()
    app.run(host='0.0.0.0', debug=True)
