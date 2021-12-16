from flask import Flask, render_template, request
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
        pas = cur.fetchall()
        if pas:
            return render_template('demo.html', pas = pas)

        else:
            return "Bhagbe chor"
        print(pas)
        mysql.connection.commit()
        cur.close()

        return 'succ'
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)