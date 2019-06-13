from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import Form,BooleanField, PasswordField, StringField, SubmitField,validators
from wtforms.validators import DataRequired
from functools import wraps
from flask import  abort ,g
from flask_login import login_user , logout_user , current_user , login_required


from passlib.hash import sha256_crypt

import psycopg2
con=psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432")
cur=con.cursor()
cur.execute("select name,username,email,password,confirm from register")
rows=cur.fetchall()

for r in rows:
    print (f"name {r[0]} username {r[1]} email {r[2]} password {r[3]} confirm {r[4]} ")


app=Flask(__name__)


@app.route("/")
def xhome():
    return render_template("xhome.html")


class RegisterForm(Form):
    
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password=form.password.data

        # Create cursor
        cur =con.cursor()

        # Execute query
        cur.execute("INSERT INTO register(name, username,email, password) VALUES(%s::varchar(20), %s::varchar(20), %s::varchar(20), %s::varchar(20))", (name,username, email,  password))

        # Commit to DB
        con.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    else:   
        return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST' :
        
        username = form.username.data
        password=form.password.data

        con=psycopg2.connect(
        database="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432")
        # Create cursor
        cur = con.cursor()

        # Get user by username
        query = "select count(*) from register where username='"+username+"' and password='"+password+"'"
        cur.execute(query)
        result1=cur.fetchone()
        
        print (result1[0])
        
        
        #for ra in result:
        if (result1[0] == 1) :
            flash('HelloUser!!!','success')
            return redirect(url_for('next')) 

        # if the above check passes, then we know the user has the right credentials
        
            
        flash('Invalid credentials','success')        
        return render_template('login.html')

    return render_template('login.html')
            # Get Form Fields
        
        

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        
        username = form.username.data
        password=form.password.data

        con=psycopg2.connect(
        database="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432")
        # Create cursor
        cur = con.cursor()

        # Get user by username
        query = "select * from register where username='admin' and password='admin'"
        cur.execute(query)
        result=cur.fetchone()
        
        print (result[0],result[1])
        
        
        #for ra in result:
        if (result[0] == username and result[1] == password) :
            flash('Admin Login','success')
            return redirect(url_for('next')) 

        # if the above check passes, then we know the user has the right credentials
        
            
        flash('You are not an admin','success')        
        return render_template('adminlogin.html')

    return render_template('adminlogin.html')


class ProductForm(Form):
    
    prodtitle = StringField('ProductTitle', [validators.Length(min=2, max=50)])
    prodprice = StringField('ProductPrice', [validators.Length(min=2, max=25)])
    prodcategory = StringField('ProductCategory', [validators.Length(min=2, max=50)])
    proddesc = PasswordField('ProductDescription',[validators.Length(min=2, max=50)])



@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = ProductForm(request.form)

    if request.method == 'POST' and form.validate() :
        prodtitle=form.prodtitle.data
        prodprice=form.prodprice.data
        prodcategory=form.prodcategory.data
        proddesc=form.proddesc.data
        
        con=psycopg2.connect(
        database="add",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432")
        
            # Create cursor
        cur =con.cursor()

            # Execute query
        cur.execute("INSERT INTO addpro(prodtitle,prodprice, prodcategory,proddesc) VALUES (%s::varchar(15),%s::varchar(15),%s::varchar(15),%s::varchar(15))" , (prodtitle,prodprice,prodcategory,proddesc))

            # Commit to DB
        con.commit()

        flash('Your Product is added', 'success')
        return redirect(url_for('search'))
    else:   
        return render_template('addproduct.html')

@app.route('/search',methods=['GET', 'POST'])
def search():
    form = ProductForm(request.form)
    if request.method == 'POST':
        
        prodtitle=form.prodtitle.data
        prodprice=form.prodprice.data
        prodcategory=form.prodcategory.data
        proddesc=form.proddesc.data
    

        con=psycopg2.connect(
        database="add",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432")
        # Create cursor
        cur = con.cursor()

        # Get user by username
        query = "select count(*) from addpro where prodtitle='"+prodtitle+"'"
        cur.execute(query)
        result=cur.fetchone()

        cur.execute("select prodtitle ,prodprice,prodcategory,proddesc from addpro where prodtitle='"+prodtitle+"'")
        row=cur.fetchall()

        for ro in row:
            print (f"prodtitle {ro[0]} prodprice {ro[1]} prodcategory {ro[2]} proddesc {ro[3]}  ")
            print(ro[0])
        
        print (result[0])

        
        #for ra in result:
        if (result[0] == 1) :
            return render_template('search.html',row=row)
             

        # if the above check passes, then we know the user has the right credential
            
        flash('Search results not ready','success')        
        return render_template('next.html')

    
    return render_template('search.html')

@app.route('/view',methods=['GET', 'POST'])
def view():
    form = ProductForm(request.form)
    if request.method == 'POST':
        
        prodtitle=form.prodtitle.data
        prodprice=form.prodprice.data
        prodcategory=form.prodcategory.data
        proddesc=form.proddesc.data
    

        con=psycopg2.connect(
        database="add",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432")
        # Create cursor
        cur = con.cursor()
         # Get user by username
        query = "select count(*) from addpro where prodtitle='"+prodtitle+"'"
        cur.execute(query)
        result=cur.fetchone()

        cur.execute("select prodtitle ,prodprice,prodcategory,proddesc from addpro where prodtitle='"+prodtitle+"'")
        res=cur.fetchall()

        for ro in res:
            print (f"prodtitle {ro[0]} prodprice {ro[1]} prodcategory {ro[2]} proddesc {ro[3]}  ")
            print(ro[0])
        
        print (result[0])

        
        #for ra in result:
        if (result[0] == 1) :
            return render_template('view.html',res=res)
             

        # if the above check passes, then we know the user has the right credential
            
        flash('Your Product is not added Properly..Check !!','danger')        
        return render_template('addproduct.html')

    
    return render_template('view.html')


               

@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out","success")
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/next")
def next():
    return render_template('next.html')




if __name__=="__main__":
    app.secret_key="1234dailywebcoding"
    app.run(debug=True)