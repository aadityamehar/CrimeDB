from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'CrimeDBfi'

mysql = MySQL(app)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        dets = request.form
        user = dets['user']
        passw = dets['pass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Police WHERE user_id = %s AND user_password = %s", (user, passw))
        global pas
        pas = cur.fetchone()
        if pas[-1] < 4:
            print(pas)
            return crime()
        else:
            return "lmao slave"

        print(pas)
        mysql.connection.commit()
        cur.close()

        return 'succ'
    return render_template('home.html')

@app.route("/crime", methods=['GET', 'POST'])
def crime():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Crime")
    crime = cur.fetchall()
    print("incrime",pas)
    return render_template('demo.html', pas=pas, paes=crime)

@app.route("/cops", methods=['GET', 'POST'])
def cops():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Police")
    police = cur.fetchall()
    if pas[-1] > 1:
        return render_template('error.html', name=pas)
    return render_template('cops.html', name=pas, paes=police)

@app.route("/prisons", methods=['GET', 'POST'])
def prisons():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Prison")
    prisons = cur.fetchall()
    return render_template('prisons.html', name=pas, paes=prisons)

@app.route("/criminals", methods=['GET', 'POST'])
def criminals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prisoner")
    criminals = cur.fetchall()
    return render_template('criminals.html', name=pas, paes=criminals)

@app.route("/fir", methods=['GET', 'POST'])
def fir():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM FIR")
    fir = cur.fetchall()
    return render_template('fir.html', name=pas, paes=fir)
    
@app.route("/addCop", methods = ['GET', 'POST'])
def addCop():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form

        cur.execute("INSERT INTO Police VALUES(%s, %s, %s, 'photo', %s, %s)", (dets['uid'], dets['name'], int(dets['phno']), dets['mail'], int(dets['rankid'])))
        mysql.connection.commit()
        cur.close()
        return redirect("/dashboard")
    return render_template('addCop.html')

if __name__ == "__main__":
    app.run(debug=True)