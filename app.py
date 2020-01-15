from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///actionsList.db'

db = SQLAlchemy(app)


class ActionsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(200), nullable=False)
    taskDetails = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(200), nullable=False)
    startDate = db.Column(db.String(200), nullable=False)
    estimatedCompletionDate = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class ProjectsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(200), nullable=False)
    projectDetails = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(200), nullable=False)
    startDate = db.Column(db.String(200), nullable=False)
    estimatedCompletionDate = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id


@app.route('/actions', methods=['POST', 'GET'])
def actions():
    if request.method == 'POST':
        taskName = request.form['taskName']
        taskDetails = request.form['taskDetails']
        owner = request.form['owner']
        priority = request.form['priority']
        startDate = request.form['startDate']
        estimatedCompletionDate = request.form['estimatedCompletionDate']
        # dateCreated = request.form['dateCreated']
        new_task = ActionsList(taskName=taskName, taskDetails=taskDetails, owner=owner, priority=priority,
                               startDate=startDate, estimatedCompletionDate=estimatedCompletionDate)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/actions')

        except:

            return 'There was an issue adding your task'

    else:
        tasks = ActionsList.query.order_by(ActionsList.dateCreated).all()
        return render_template("/actions.html", tasks=tasks)


@app.route('/actions/delete/<int:id>')
def delete(id):
    task_to_delete = ActionsList.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/actions')
    except:
        return 'There was a problem deleting that task'


@app.route('/actions/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = ActionsList.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.taskName = request.form['taskName']
        task_to_update.taskDetails = request.form['taskDetails']
        task_to_update.owner = request.form['owner']
        task_to_update.priority = request.form['priority']
        task_to_update.startDate = request.form['startDate']
        task_to_update.estimatedCompletionDate = request.form['estimatedCompletionDate']

        try:
            db.session.commit()
            return redirect('/actions')
        except:
            return 'There was a problem updating your task'

    else:
        return render_template('update.html', task_to_update=task_to_update)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/projects', methods=['POST', 'GET'])
def projects():
    if request.method == 'POST':
        projectName = request.form['projectName']
        projectDetails = request.form['projectDetails']
        owner = request.form['owner']
        priority = request.form['priority']
        startDate = request.form['startDate']
        estimatedCompletionDate = request.form['estimatedCompletionDate']
        # dateCreated = request.form['dateCreated']
        new_project = ProjectsList(projectName=projectName, projectDetails=projectDetails, owner=owner, priority=priority,
                                   startDate=startDate, estimatedCompletionDate=estimatedCompletionDate)

        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect('/projects')

        except:

            return 'There was an issue adding your project'

    else:
        projects = ProjectsList.query.order_by(ProjectsList.dateCreated).all()
        return render_template("/projects.html", projects=projects)


@app.route('/projects/delete/<int:id>')
def project_delete(id):
    project_to_delete = ProjectsList.query.get_or_404(id)

    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/projects')
    except:
        return 'There was a problem deleting that project'


@app.route('/projects/projectUpdate/<int:id>', methods=['GET', 'POST'])
def project_update(id):
    project_to_update = ProjectsList.query.get_or_404(id)
    if request.method == 'POST':
        project_to_update.projectName = request.form['projectName']
        project_to_update.projectDetails = request.form['projectDetails']
        project_to_update.owner = request.form['owner']
        project_to_update.priority = request.form['priority']
        project_to_update.startDate = request.form['startDate']
        project_to_update.estimatedCompletionDate = request.form['estimatedCompletionDate']

        try:
            db.session.commit()
            return redirect('/projects')
        except:
            return 'There was a problem updating your project'

    else:
        return render_template('projectUpdate.html', project_to_update=project_to_update)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
