from app import app
from models import Project, TestSuit

@app.route('/projects/<int:project_id>')
def project(project_id):
    project = Project.query.get(project_id)
    return render_template('project.html', project=project)

@app.route('/test_suits/<int:test_suit_id>')
def test_suit(test_suit_id):
    test_suit = TestSuit.query.get(test_suit_id)
    return render_template('test_suit.html', test_suit=test_suit)