from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #tells the app where the database is located
db = SQLAlchemy(app) #initialize database

#table structure
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# define a route for home page
@app.route('/',methods=['POST','GET'])
def index(): #method that runs when home page is accessed
    if request.method == 'POST':
        task_content = request.form['content'] #get content from form
        new_task = Todo(content=task_content) #create new task object

        try:
            db.session.add(new_task) #add task to database session
            db.session.commit() #commit changes to database
            return redirect('/') #redirect to home page
        
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks=Todo.query.order_by(Todo.date_created).all() #query all tasks from database ordered by date created
        return render_template('index.html',tasks=tasks) #loads index.html from templates folder

@app.route('/delete/<int:id>')
def delete(id): #function to delete a task by id
    task_to_delete = Todo.query.get_or_404(id) #get task by id or return 404 if not found

    try:
        db.session.delete(task_to_delete) #delete task from database session
        db.session.commit() #commit changes to database
        return redirect('/') #redirect to home page
    
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
        
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True) #auto reload on changes
    