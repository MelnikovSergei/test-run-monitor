from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://user:password@db:5432/database'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from models import Project, TestSuit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        name = request.form['name']
        project = Project(name=name)
        db.session.add(project)
        db.session.commit()
        return f'Project {name} created successfully!'
    return render_template('new_project.html')

@app.route('/test_suits')
def test_suits():
    test_suits = TestSuit.query.all()
    return render_template('test_suits.html', test_suits=test_suits)

@app.route('/test_suits/new', methods=['GET', 'POST'])
def new_test_suit():
    if request.method == 'POST':
        name = request.form['name']
        test_suit = TestSuit(name=name)
        db.session.add(test_suit)
        db.session.commit()
        return f'Test suit {name} created successfully!'
    return render_template('new_test_suit.html')

if __name__ == '__main__':
    app.run(debug=True)
    