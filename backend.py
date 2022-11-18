from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'xxxx'
app.config['MYSQL_PASSWORD'] = 'xxxx'
app.config['MYSQL_DB'] = 'CrimeDBfi'

mysql = MySQL(app)

@app.route("/home", methods = ['GET', 'POST'])
def home():
    return render_template('main.html')

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
        if pas:
            if pas[-1] < 4:
                print(pas)
                return redirect("/dashboard")
            else:
                return "Error"
        else:
            return redirect("/noUser")

        print(pas)
        mysql.connection.commit()
        cur.close()
    return render_template('home.html')

@app.route("/crime", methods=['GET', 'POST'])
def crime():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Crime")
    crime = cur.fetchall()
    print("incrime", pas)
    return render_template('demo.html', pas=pas, paes=crime)

@app.route("/noUser", methods=['GET', 'POST'])
def noUser():
    return render_template('noUser.html')

@app.route("/cops", methods=['GET', 'POST'])
def cops():
    if pas[-1] > 1:
        return redirect('/error')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Police")
    police = cur.fetchall()
    return render_template('cops.html', name=pas, paes=police)

@app.route("/error", methods=['GET', 'POST'])
def error():
    return render_template('error.html', name=pas)

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

@app.route("/courts", methods=['GET', 'POST'])
def courts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Court")
    courts = cur.fetchall()
    return render_template('courts.html', name=pas, paes=courts)

@app.route("/victims", methods=['GET', 'POST'])
def victims():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Victim")
    victims = cur.fetchall()
    return render_template('victims.html', name=pas, paes=victims)

@app.route("/crimeVictims", methods=['GET', 'POST'])
def crimeVictims():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CrimeVictims")
    victims = cur.fetchall()
    return render_template('CrimeVictims.html', name=pas, paes=victims)

@app.route("/crimeCriminals", methods=['GET', 'POST'])
def crimeCriminals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CrimePrisoner")
    victims = cur.fetchall()
    return render_template('crimeCriminals.html', name=pas, paes=victims)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT c_type, count(c_type) FROM prisonerFelony WHERE c_dnt > '2021-01-01' GROUP BY c_type")
    crimeoc = cur.fetchall()
    cur.execute("SELECT c_place, count(c_place) from crime group by c_place")
    lococ = cur.fetchall()
    print("incrime",pas)
    return render_template('dashboard.html', name=pas, paes=crimeoc, paes1 = lococ)

@app.route("/addCop", methods = ['GET', 'POST'])
def addCop():
    if pas[-1] > 1:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        if "uid" in dets.keys():        
            cur.execute("INSERT INTO Police VALUES(%s, %s, %s, 'photo', %s, %s)", (dets['uid'], dets['name'], int(dets['phno']), dets['mail'], int(dets['rankid'])))
        if "deluid" in dets.keys():
            cur.execute("DELETE from Police where user_id = %s", (dets["deluid"],))
        mysql.connection.commit()
        cur.close()
        return redirect("/cops")
    return render_template('addCop.html')

@app.route("/addCrime", methods = ['GET', 'POST'])
def addCrime():
    if pas[-1] > 4:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
    
        if dets["date"] != "":
            cur.execute("INSERT INTO Crime VALUES(%s, %s, %s, %s, %s, %s, 'Active')", (dets['uid'], dets['date'], dets['location'], dets['description'], dets['description'], dets['court']))
        if dets["vid"] != "":
            cur.execute("INSERT INTO CrimeVictims VALUES(%s, %s)", (dets["uid"], dets["vid"]))
        if dets["pid"] != "":
            cur.execute("INSERT INTO CrimePrisoner VALUES(%s, %s)", (dets["pid"], dets["uid"]))
        mysql.connection.commit()

        cur.close()
        return redirect("/crime")
    return render_template('addCrime.html')

@app.route("/addCourt", methods = ['GET', 'POST'])
def addCourt():
    if pas[-1] > 1:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        cur.execute("INSERT INTO Court VALUES(%s, %s, %s)", (dets['uid'], dets['address'], dets['name']))
        mysql.connection.commit()
        cur.close()
        return redirect("/courts")
    return render_template('addCourt.html')

@app.route("/addPrison", methods = ['GET', 'POST'])
def addPrison():
    if pas[-1] > 1:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        if "uid" in dets.keys():
            cur.execute("INSERT INTO Prison VALUES(%s, %s, %s, %s)", (dets['uid'], dets['warden'], dets['address'], dets['name']))
        
        mysql.connection.commit()
        cur.close()
        return redirect("/prisons")
    return render_template('addPrison.html')

@app.route("/addVictim", methods = ['GET', 'POST'])
def addVictim():
    if pas[-1] > 4:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        cur.execute("INSERT INTO Victim VALUES(%s, %s, %s, %s, %s)", (dets['uid'], dets['name'], int(dets['phno']), dets['sex'], dets['address'],))
        mysql.connection.commit()
        cur.close()
        return redirect("/victims")
    return render_template('addVictim.html')

@app.route("/addCriminal", methods = ['GET', 'POST'])
def addCriminal():
    if pas[-1] > 4:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        cur.execute("INSERT INTO Prisoner VALUES(%s, %s, %s, %s, %s, %s, null)", (dets['uid'], dets['name'], int(dets['sentence']), dets['dob'], dets['doi'], dets['address'],))
        mysql.connection.commit()
        cur.close()
        return redirect("/criminals")
    return render_template('addCriminal.html')

@app.route("/addFIR", methods = ['GET', 'POST'])
def addFIR():
    if pas[-1] > 2:
        return redirect('/error')
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        cur.execute("INSERT INTO FIR VALUES(%s, %s, %s)", (dets['cid'], dets['fid'], dets['description'],))
        mysql.connection.commit()
        cur.close()
        return redirect("/fir")
    return render_template('addFIR.html')


@app.route("/closeCrime", methods = ['GET', 'POST'])
def closeCrime():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        dets = request.form
        cur.execute("UPDATE Crime set c_status = 'Closed' where c_id = %s", (dets['uid'],))
        cur.execute("UPDATE Prisoner set p_sentence = %s where p_id = %s", (dets['sentence'], dets['cid']))
        mysql.connection.commit()
        cur.close()
        return redirect("/crime")
    return render_template('closeCrime.html')


if __name__ == "__main__":
    app.run(debug=True)
