from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    student_class = db.Column(db.String(20))


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(20), unique=True)

    student_name = db.Column(db.String(100))

    father_name = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    student_class = db.Column(db.String(20))

    monthly_fee = db.Column(db.Integer, default=1000)

@app.route("/")
def home():
    return render_template("home.html")

# REPLACE THIS SECTION
@app.route("/admission", methods=["GET", "POST"])
def admission():

    if request.method == "POST":

        new_admission = Admission(
            student_name=request.form["student_name"],
            dob=request.form["dob"],
            father_name=request.form["father_name"],
            mother_name=request.form["mother_name"],
            phone=request.form["phone"],
            address=request.form["address"],
            student_class=request.form["student_class"]
        )

        db.session.add(new_admission)
        db.session.commit()

        return render_template("success.html")

    return render_template("admission.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "bal123":

            return render_template(
                "admin.html",
                admissions=Admission.query.all()
            )

        return "Invalid Login"

    return render_template("login.html")
@app.route("/admin")
def admin():

    admissions = Admission.query.all()

    return render_template(
        "admin.html",
        admissions=admissions
    )
@app.route("/students")
def students():

    students = Student.query.all()

    return render_template(
        "students.html",
        students=students
    )
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)