from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle
import pandas as pd
import pandas as pd
import re 
from flask import Flask, redirect, url_for, request, render_template
 
import pickle
 
import numpy as np # linear algebra
import pandas as pd  

from sklearn.feature_extraction.text import CountVectorizer
 
import re
import pickle
import numpy as np 
import pickle
import itertools
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
app = Flask(__name__)
# read object TfidfVectorizer and model from disk
pickle_in = open('vote.pickle','rb')
pac = pickle.load(pickle_in)
tfid = open('tfid.pickle','rb')
tfidf_vectorizer = pickle.load(tfid)

app.secret_key = 'neha'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'vote'
mysql = MySQL(app)

@app.route('/',methods = ['GET','POST'])
def first():
    return render_template('first.html')
 
 
  
@app.route('/loginad') 
def loginad():
	return render_template('loginad.html')
    
@app.route('/upload') 
def upload():
	return render_template('upload.html') 
@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)


@app.route('/login', methods = ['GET',"POST"])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM people WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            global Id
            session['Id'] = account['Id']
              
            Id = session['Id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('profile'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password! Please login with correct credentials')
            return redirect(url_for('login'))
    # Show the login form with message (if any)

    return render_template('login.html', msg=msg)

@app.route('/register',methods= ['GET',"POST"])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
      
        
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
        pattern = re.compile(reg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account exists using MySQL)
        cursor.execute('SELECT * FROM people WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.search(pattern,password):
            msg = 'Password should contain atleast one number, one lower case character, one uppercase character,one special symbol and must be between 6 to 10 characters long'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO people VALUES (NULL, %s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            flash('You have successfully registered! Please proceed for login!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return msg
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/index')
def index():
 	return render_template("index.html")

 

@app.route('/sandy',methods=['POST','GET'])
def sandy():
  
    if request.method == 'POST':    
        
        query_content=request.form['news_content']
        
        total= query_content
        total = re.sub('<[^>]*>', '', total)
        total = re.sub(r'[^\w\s]','', total)
        total = total.lower()     
        data=[total]
        vect=tfidf_vectorizer.transform(data).toarray()
        prediction=pac.predict(vect)
        pred=format(prediction[0])
   
        login()
        details = request.form
        
        news_content = details['news_content']
        parties_name = details['parties_name']
        
         
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO review(news_content,pred,userid,parties_name) VALUES ( %s, %s,%s,%s) ", (news_content,pred,Id,parties_name))
         
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
         
 
         
     
         
    return render_template('index.html') 
@app.route('/users')
def users():
     
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" SELECT * from people INNER JOIN review ON people.ID = review.USERID ")
     
    if resultValue > 0:
        userDetails = cur.fetchall()
         
        return render_template('users.html',userDetails=userDetails)
@app.route('/profile')    
def profile():
    
     
         
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM people WHERE Id = %s', (Id,))
        account = cursor.fetchone()
       
        return render_template('profile.html', account=account)             
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" SELECT * from people INNER JOIN review ON people.ID = review.USERID;")
     
    if resultValue > 0:
        userDetails = cur.fetchall()
         
        return render_template('admin.html',userDetails=userDetails)  
@app.route('/userdetail')
def userdetail():  
   cur = mysql.connection.cursor()      
   cur.execute("SELECT * from people")
   useradmin=cur.fetchall()
   print(useradmin)
       
   return render_template('userdetail.html',useradmin=useradmin)         
@app.route('/chart')
def chart():
    legend = "review by parties_name"
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows1 = cursor.fetchall()
        labels = list()
        i = 0
        for row1 in rows1:
            labels.append(row1[i])
         

         
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows2 = cursor.fetchall()
        
        label = list()
        j = 0
        values = list()
        k = 0
        for row2 in rows2:
            label.append(row2[j])
            cursor.execute("SELECT COUNT(id) from review WHERE  pred = 'Neutral' and parties_name=%s", (row2[j],))
            rows3 = cursor.fetchall()
             
            #j=j+1
        # Convert query to objects of key-value pairs
            
            for row3 in rows3:
	              values.append(row3[k])
            #k=k+1
        mysql.connection.commit()
        cursor.close()
        
        
        
    except:
        print('Error: unable to fetch items')    

    return render_template('chart.html', values=values, labels = labels, legend=legend)
@app.route('/sadness')
def sadness():
    legend = "review by parties_name"
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows1 = cursor.fetchall()
        labels = list()
        i = 0
        for row1 in rows1:
            labels.append(row1[i])
         

         
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows2 = cursor.fetchall()
        
        label = list()
        j = 0
        values = list()
        k = 0
        for row2 in rows2:
            label.append(row2[j])
            cursor.execute("SELECT COUNT(id) from review WHERE  pred = 'Negative' and parties_name=%s", (row2[j],))
            rows3 = cursor.fetchall()
             
            #j=j+1
        # Convert query to objects of key-value pairs
            
            for row3 in rows3:
	              values.append(row3[k])
            #k=k+1
        mysql.connection.commit()
        cursor.close()
        
        
        
    except:
        print('Error: unable to fetch items')    

    return render_template('sadness.html', values=values, labels = labels, legend=legend) 
@app.route('/worry')
def worry():
    legend = "review by parties_name"
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows1 = cursor.fetchall()
        labels = list()
        i = 0
        for row1 in rows1:
            labels.append(row1[i])
         

         
        cursor.execute("SELECT parties_name from review GROUP BY parties_name")
        # data = cursor.fetchone()
        rows2 = cursor.fetchall()
        
        label = list()
        j = 0
        values = list()
        k = 0
        for row2 in rows2:
            label.append(row2[j])
            cursor.execute("SELECT COUNT(id) from review WHERE  pred = 'Positive' and parties_name=%s", (row2[j],))
            rows3 = cursor.fetchall()
             
            #j=j+1
        # Convert query to objects of key-value pairs
            
            for row3 in rows3:
	              values.append(row3[k])
            #k=k+1
        mysql.connection.commit()
        cursor.close()
        
        
        
    except:
        print('Error: unable to fetch items')    

    return render_template('worry.html', values=values, labels = labels, legend=legend)     
    
    
@app.route('/pie') 
def pie():
	return render_template('pie.html') 
    
if __name__ == '__main__':
    app.run()