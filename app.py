from flask import Flask , render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__) # setting up our application ,__name__ is referencing this file

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

database = SQLAlchemy(app)

class Todo(database.Model):
    id = database.Column(database.Integer , primary_key = True)
    content = database.Column(database.String(200), nullable = False)
    date_created = database.Column(database.DateTime, default = datetime.utcnow)

def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) # creating index route 

def index (): # function to define the index route
    if request.method == 'POST':
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        try:
            database.session.add(new_task)
            database.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your request"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks)


@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        database.session.delete(task_to_delete)
        database.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleteing that task"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    task = Todo.query.get_or_404(id)
    if request.method =='POST':
       task.content = request.form['content']
       try:
           database.session.commit()
           return redirect('/')
       except:
           return "There was an issue updating your task"
    else:
        return render_template('update.html',task=task )
if __name__ == "__main__":
    app.run(debug=True)
