from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:VasmiGroup#123@localhost:5432/js'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key in a real application

db = SQLAlchemy(app)
# db.init_app(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    full_name = db.Column(db.Text, nullable = False)
    mobile = db.Column(db.Text, nullable = False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=True)
    dob = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<users {self.full_name}>'


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_name = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.Text, nullable=False)
    insurance_type = db.Column(db.Text)
    company_name = db.Column(db.Text)
    policy_np = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Claim {self.policy_no}>'


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_name = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer)
    mobile = db.Column(db.Text, nullable=False)
    updates = db.Column(db.Boolean, default = False, nullable=False)
    email = db.Column(db.Text)
    appointment = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Appointment {self.customer_name}>'

@app.route("/")
def hello():
    # data = users.query.first()
    # return data
    return "Homepage"

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    print("request type method:", request.method)
    if request.method == 'POST':
        print("request type method:", request.method)
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        email = request.form['email']
        dob = request.form['dob']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        print('*'*50)
        print('hashed_password:',hashed_password)
        new_user = users(full_name=username ,mobile = mobile, password=hashed_password, dob = dob, email = email)

        db.session.add(new_user)
        print('*'*50)
        print(db.session.commit())

        # return "<h2>Registration Successfull</h2>"
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']

        user = users.query.filter_by(mobile=mobile).first()

        if user and check_password_hash(user.password, password):
            return 'Login successful!'
        else:
            return 'Login failed. Please check your username and password.'

    return render_template('login.html')

# Saving Policy Claim Requests
@app.route('/claims', methods=['GET','POST'])
def claims():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        mobile = request.form['mobile']
        insurance_type = request.form['insurance_type']
        company_name = request.form['company_name']
        policy_no = request.form['policy_no']

        new_claim = Claim(customer_name = customer_name, mobile = mobile, insurance_type = insurance_type, company_name = company_name, policy_np = policy_no)

        db.session.add(new_claim)
        print('*'*50)
        db.session.commit()

        return "<h2> Claims Saved! </h2>"


    return render_template('claims.html')

# Saving Appointment Requests
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        customer_name = request.form['username']
        dob = request.form['dob']
        age = request.form['age']
        mobile = request.form['mobile']
        updates = request.form.get('updates') == "True"
        print('#'*50)
        print('updates ---', updates)
        print('#'*50)
        email = request.form['email']
        appointment = request.form['appointment_date']

        new_appointment = Appointments(
            customer_name = customer_name,
            dob = dob,
            age = age,
            mobile = mobile,
            updates = updates,
            email = email,
            appointment = appointment)
        db.session.add(new_appointment)
        db.session.commit()
    
    all_appointments = Appointments.query.all()
    return render_template('appointments.html', appointments = all_appointments)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)