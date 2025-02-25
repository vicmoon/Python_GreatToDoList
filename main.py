from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from wtforms import StringField, SubmitField, SelectField
from sqlalchemy import Column, Integer, String
from wtforms.validators import DataRequired


app = Flask(__name__)


#create todos database 
class Base(DeclarativeBase):
    pass


app.config['SECRET_KEY'] = "238043rjierhg95"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todoes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


#Add new ToDo Form 

class NewToDoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    progress = SelectField(
        'Progress',
        choices=[
        ('new', 'New'), 
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Add')




#To Do Table Configuration 

class ToDo(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)  
    details = Column(String(500), nullable=False)  
    progress = Column(String(50), nullable=False)  



# Create tables
with app.app_context():
    db.create_all()





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    form = NewToDoForm()

    if form.validate_on_submit():
        new_todo = ToDo(name=form.name.data, details=form.details.data, progress=form.progress.data)
        db.session.add(new_todo)
        db.session.commit()
        return render_template("index.html")  
    return render_template("add.html", form=form)





if __name__ == '__main__':
    app.run(debug=True)
