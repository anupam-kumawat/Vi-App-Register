from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import re
import MySQLdb.cursors
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Anupam'
app.config['MYSQL_PASSWORD'] = '8955@Mysql'
app.config['MYSQL_DB'] = 'vi_live'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        if (username == 'ankit' and password == '1234' ):
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = 'ankit'
            msg = 'Logged in successfully !'
            return render_template('register.html')
        
        else: 
            msg = 'Incorrect username / password'
        
        
        
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM login_user WHERE name = %s AND password = %s', (username,password,))
        # account = cursor.fetchone()
        
        # if account:
        #     session['loggedin'] = True
        #     session['id'] = account['sno']
        #     session['username'] = account['name']
        #     msg = 'Logged in successfully !'
        #     return render_template('register.html', msg=msg)
        
        # else: 
        #     msg = 'Incorrect username / password'
            
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

     
@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'mobile' in request.form and 'district_id' in request.form and 'created_at' in request.form and 'updated_at' in request.form:
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        district_id = request.form['district_id']
        
        password = request.form['password']
        password_text = request.form['password_text']
        
        created_at = request.form['created_at']
        updated_at = request.form['updated_at']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE mobile = %s', (mobile,))
        user = cursor.fetchone()
        
        if user:
            msg = 'Account already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address !'
        # elif not re.match(r'[A-Za-z0-9]+', name):
        #     msg = 'Username must contain only characters and numbers !'
        elif not name or not email or not mobile or not district_id:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, NULL, NULL, %s, NULL, 0, NULL, %s, %s, NULL, %s, %s)', (name, email, mobile, district_id, password, password_text, created_at, updated_at))
            mysql.connection.commit()
            msg = 'You have successfully reigstered !'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        
    return render_template('register.html', msg=msg)


@app.route('/users', methods=['GET','POST'])
def users():

    sql = ('SELECT * FROM users')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    
    allUsers = cursor.fetchall()
    
    return render_template('users.html', allUsers=allUsers)


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST' and 'username' in request.form :  #for search function
        name = request.form['username']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s OR name = %s OR mobile = %s', (name,name,name, ))
    
        allUsers = cursor.fetchall()
        
        return render_template('search.html', allUsers=allUsers)


if __name__ == '__main__':
    app.run(debug=True)
            
        