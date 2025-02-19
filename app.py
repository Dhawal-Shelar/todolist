from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(550), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.sno} -> {self.title}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>", methods=['POST'])
def delete(sno):
    todo = Todo.query.get(sno)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
