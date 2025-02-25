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



class NewToDoForm(FlaskForm):
    name = StringField('Do what?', validators=[DataRequired()])
    
    progress = SelectField(
        'State',
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
    name = Column(String(250), nullable=False)  
    progress = Column(String(50), nullable=False)  



# Create tables
with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/all')
def get_todo():
    all_todoes = ToDo.query.all()
    if not all_todoes:
        return render_template("error.html")


    return render_template("alltodoes.html", todoes = all_todoes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = NewToDoForm()
    if form.validate_on_submit():
        print("Form validated!")  # ✅ Debugging step

        new_todo = ToDo(
            name=form.name.data,
            progress=form.progress.data
        )
        db.session.add(new_todo)
        db.session.commit()
        print("New ToDo added:", new_todo.name)  # ✅ Debugging step

        return redirect(url_for("home"))

    print("Form validation failed.")  # ✅ Debugging step
    return render_template("add.html", form=form)




@app.route("/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    todo = ToDo.query.get(todo_id)

    if not todo:
        return "No such ToDo found", 404
    

    data = request.get_json()
    action = data.get("action")

    if action == "done":
        todo.progress = "done"
        db.session.commit()
        return redirect(url_for("home"))

    elif action == "delete":
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("home"))

    # return jsonify({"error": "Invalid action"}), 400
    



if __name__ == '__main__':
    app.run(debug=True)
