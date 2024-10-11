from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    test_suits = db.relationship('TestSuit', backref='project', lazy=True)

    def __repr__(self):
        return f'Project({self.name})'

class TestSuit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='not_run')
    last_result = db.Column(db.String(100), nullable=False, default='')
    execution_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'TestSuit({self.status})'
    