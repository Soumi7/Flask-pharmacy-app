import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../medidatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Medicine(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        medicine = Medicine(name=request.form.get("name"))
        db.session.add(medicine)
        db.session.commit()
    medicines = Medicine.query.all()
    return render_template("home.html", medicines=medicines)

@app.route("/delete", methods=["POST"])
def delete():
    name=request.form.get("name")
    medicine = Medicine.query.filter_by(name=name).first()
    db.session.delete(medicine)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()