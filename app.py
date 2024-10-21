from datetime import datetime
from email.policy import default

from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///TODO.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f'{self.sno}-{self.title}'

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        title=request.form['title']
        desc=request.form['desc']

    # To Save the data to the database
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    # fetch the data from db
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/edit/<int:sno>',methods=['GET','POST'])
def edit(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']

        # update the data
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete_data(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # deleted_Todo=Todo.query.delete(sno)
    # print(allTodo)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=8000)