from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///actionsList.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


# class ActionsList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     taskName = db.Column(db.String(200), nullable=True)
#     taskDetails = db.Column(db.String(200), nullable=True)
#     owner = db.Column(db.String(200), nullable=True)
#     priority = db.Column(db.String(200), nullable=True)
#     startDate = db.Column(db.String(200), nullable=True)
#     estimatedCompletionDate = db.Column(db.String(200), nullable=True)
#     dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id


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


@app.route('/', methods=['POST', 'GET'])
def index():
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
            return redirect('/')

        except:

            return 'There was an issue adding your task'

    else:
        tasks = ActionsList.query.order_by(ActionsList.dateCreated).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ActionsList.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
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
            return redirect('/')
        except:
            return 'There was a problem updating your task'

    else:
        return render_template('update.html', task_to_update=task_to_update)


@app.route('/actions')
def actions():
    return render_template('actions.html')


if __name__ == "__main__":
    app.run(debug=True)
