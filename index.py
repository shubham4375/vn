from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date
from werkzeug.utils import secure_filename

import base64
import PIL.Image as Image
import io
import os

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import webbrowser

from werkzeug.datastructures import ContentRange

app=Flask(__name__)

app.secret_key = "your secret key"


app.config['MYSQL_HOST'] = "restaurant.c52jrjvcdvgp.us-east-2.rds.amazonaws.com"
app.config['MYSQL_USER'] = "admin"
app.config['MYSQL_PASSWORD'] ="Sysintello#2141"
app.config['MYSQL_DB'] = "project"
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration' , methods=[ 'GET','POST' ])
def registration():
    msg = ''
    if request.method == 'POST':
        userid=session['loginid']
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phone_number']
        gender = request.form['gender']
        age = request.form['age']
        style = request.form['style']
        beginner = request.form['beginner']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registration WHERE name = % s',(name, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif request.method == 'POST':
            cursor.execute('INSERT INTO registration (userid,name,address,email,phone_number,gender,age,style,beginner) VALUES (% s,% s,% s,% s,% s,% s,% s,% s,% s)',(userid,name,address,email,phone_number,gender,age,style,beginner))
            mysql.connection.commit()
            session['alreadyregistered'] = True
            msg = "thank you !"
            return render_template('batches.html')
    elif request.method =='POST':
        msg = 'fill up form'
    return render_template('registration.html' ,msg=msg)

@app.route('/style')
def style():
    return render_template('style.html')

@app.route('/batch' )
def batches():
    # msg = ''
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM kids')
    # kidsdata = cursor.fetchall()

    # cursor.execute('SELECT * FROM junior')
    # juniordata = cursor.fetchall()

    # cursor.execute('SELECT * FROM women')
    # womendata = cursor.fetchall()

    # cursor.execute('SELECT * FROM adult')
    # adultdata = cursor.fetchall()

    # cursor.execute('SELECT * FROM couple')
    # coupledata = cursor.fetchall()

    # cursor.execute('SELECT * FROM fitness')
    # fitnessdata = cursor.fetchall()
     
    # return render_template('batches.html',kidsdata=kidsdata,juniordata=juniordata,womendata=womendata,adultdata=adultdata,coupledata=coupledata,fitnessdata=fitnessdata)
    return render_template('batches.html')

@app.route('/kids')
def kids():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM kids')
    kidsdata = cursor.fetchall()
    if 'loggedin' in session:
        return render_template('kids.html',kidsdata=kidsdata)
    else:
        return render_template('loginsector.html')


@app.route('/junior')
def junior():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM junior')
    juniordata = cursor.fetchall()
    if 'loggedin' in session:
        return render_template('junior.html',juniordata=juniordata)
    else:
        return render_template('loginsector.html')

@app.route('/adult')
def adult():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM adult')
    adultdata = cursor.fetchall()

    if 'loggedin' in session:
        return render_template('adult.html',adultdata=adultdata)
    else:
        return render_template('loginsector.html')


@app.route('/women')
def women():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM women')
    womendata = cursor.fetchall()


    if 'loggedin' in session:
        return render_template('women.html',womendata=womendata)
    else:
        return render_template('loginsector.html')


   

@app.route('/fitness')
def fitness():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM fitness')
    fitnessdata = cursor.fetchall()


    if 'loggedin' in session:
        return render_template('fitness.html',fitnessdata=fitnessdata)
    else:
        return render_template('loginsector.html')


    

@app.route('/couple')
def couple():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM couple')
    coupledata = cursor.fetchall()


    if 'loggedin' in session:
        return render_template('couple.html',coupledata=coupledata)
    else:
        return render_template('loginsector.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/img')
def img():
    return render_template('img.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=[ 'GET','POSt' ])
def contact():
    msg = ''
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        number = request.form['number']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM contact WHERE firstname = % s',(firstname, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif request.method == 'POST':
            cursor.execute('INSERT INTO contact VALUES (% s,% s,% s,% s,% s)',(firstname,lastname,email,number,message))
            mysql.connection.commit()
            msg = "thank you !"
            return render_template('home.html')
    elif request.method =='POST':
        msg = 'fill up form'
    return render_template('contact.html' ,msg=msg)

@app.route('/video')
def video():
    if 'loggedin' in session:
        return render_template('video.html')
    else:
        return render_template('loginsector.html')

@app.route('/event')
def event():
    if 'loggedin' in session:
        return render_template('event.html')
    else:
        return render_template('loginsector.html')


@app.route('/workshop')
def workshop():
    if 'loggedin' in session:
        return render_template('workshop.html')
    else:
        return render_template('loginsector.html')


@app.route('/login'  , methods = ['GET' , 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE username = % s AND password = % s', (username,password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['loginid'] = account['loginid']
            session['email'] = account['email']
            return render_template('home.html', msg = msg)
        else:
            msg = 'Sorry, your password was incorrect. Please double-check your password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    session.clear()
    return redirect(url_for('home'))

@app.route('/signup' , methods =['GET' , 'POST'])
def signup():
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM signup WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO signup (username, password, email) VALUES (% s, % s, % s)', (username, password, email)) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

# @app.route('/time')
# def time():
#     return render_template('#.html')
#admin panel

@app.route('/home')
def home1():
    return render_template('home1.html')

@app.route('/registration2')
def registration2():
    return render_template('registration2.html')

@app.route('/style2')
def style2():
    return render_template('style2.html')

@app.route('/batch2')
def batches2():
    return render_template('batches2.html')

@app.route('/layout2')
def layout2():
    return render_template('layout2.html')

@app.route('/contact2', methods=[ 'GET','POSt' ])
def contact2():
    msg = ''
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        number = request.form['number']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM contact WHERE firstname = % s',(firstname, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif request.method == 'POST':
            cursor.execute('INSERT INTO contact VALUES (% s,% s,% s,% s,% s)',(firstname,lastname,email,number,message))
            mysql.connection.commit()
            msg = "thank you !"
            return render_template('home.html')
    elif request.method =='POST':
        msg = 'fill up form'
    return render_template('contact2.html' ,msg=msg)

@app.route('/video2')
def video2():
        return render_template('video2.html')

@app.route('/event2')
def event2():
    userid = session['loginid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select registration.name, registration.email, registration.phone_number, registration.style, batchtime.batchtime,batchtime.batchdate from registration inner join batchtime on registration.userid = batchtime.userid where registration.userid = %s and batchtime.userid = %s;",(userid,userid))
    data = cursor.fetchall()
    mysql.connection.commit()


    return render_template('event2.html',data=data)

@app.route('/workshop2')
def workshop2():
    return render_template('workshop2.html')



@app.route('/addbatchtime', methods=[ 'GET','POST' ])
def addbatchtime():
    msg = ''
    if request.method == 'POST':
        userid=session['loginid']
        batchtime = request.form['batchtime']
        today = date.today()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO batchtime(userid,batchtime,batchdate) VALUES (% s,% s,% s)',(userid,batchtime,today))
        mysql.connection.commit()
        session['alreadybatchconfirm'] = True

    return redirect(url_for('.event2'))










































#=======================ADMIN login start=============================================

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
  msg = ''

  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM adminlogin WHERE adminusername = %s AND adminpassword = %s ', (username, password))
    account = cursor.fetchone()
    if account:
      session['adminloggedin'] = True
      session['adminname'] = account['adminusername']
      session['adminid'] = account['adminid']

      return redirect(url_for('adminhome'))
    else:
      msg = 'Incorrect username / password !'
  return render_template('adminlogin.html', msg=msg)


#=======================admin login end====================================================================







@app.route('/adminhome')
def adminhome():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM signup ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        signupcount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM registration ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        registrationcount=value
    cursor.close()
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM kids ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        kidscount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM junior ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        juniorcount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM adult ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        adultcount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM women ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        womencount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM fitness ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        fitnesscount=value
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM couple ")
    data =cursor.fetchall()
    new_data=data[0]
    for key,value in new_data.items():
        couplecount=value
    cursor.close()
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='Breakfast' and unitid=%s ",[unitid])
    # product =cur.fetchall()
    # new_product=product[0]
    # for key,value in new_product.items():
    #     breakfast_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='desserts'and unitid=%s",[unitid])
    # dessert =cur.fetchall()
    # new_dessert=dessert[0]
    # for key,value in new_dessert.items():
    #     dessert_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='fastfood'and unitid=%s",[unitid])
    # fastfood =cur.fetchall()
    # new_fastfood=fastfood[0]
    # for key,value in new_fastfood.items():
    #     fastfood_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='drinks'and unitid=%s",[unitid])
    # drinks =cur.fetchall()
    # new_drinks=drinks[0]
    # for key,value in new_drinks.items():
    #     drinks_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='snacks'and unitid=%s",[unitid])
    # snacks =cur.fetchall()
    # new_snacks=snacks[0]
    # for key,value in new_snacks.items():
    #     snacks_count=value
    # cur.close()
    #
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='coffee'and unitid=%s",[unitid])
    # coffee =cur.fetchall()
    # new_coffee=coffee[0]
    # for key,value in new_coffee.items():
    #     coffee_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='chinese'and unitid=%s",[unitid])
    # chinese =cur.fetchall()
    # new_chinese=chinese[0]
    # for key,value in new_chinese.items():
    #     chinese_count=value
    # cur.close()
    #
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT COUNT(*) FROM product where category='continental'and unitid=%s",[unitid])
    # continental =cur.fetchall()
    # new_continental=continental[0]
    # for key,value in new_continental.items():
    #     continental_count=value
    # cur.close()
    #



    return render_template("icon-menu.html", signupcount=signupcount , registrationcount=registrationcount , kidscount=kidscount , juniorcount=juniorcount , adultcount=adultcount , womencount=womencount , fitnesscount=fitnesscount , couplecount=couplecount )





@app.route('/adminlogout')
def adminlogout():
  session.pop('adminloggedin', None)
  session.pop('adminid', None)
  session.pop('adminname', None)
  session.pop('adminunitid',None)
  return redirect(url_for('adminlogin'))


@app.route('/userdetails')
def userdetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from signup")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('userdetails.html', userdetails=rows)




@app.route("/insertuserdetails",methods=["POST","GET"])
def insertuserdetails():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        cur.execute("INSERT INTO signup (username,password, email) VALUES (%s, %s, %s)",[username,password, email])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/userdetails')




@app.route('/updateuserdetails',methods=['POST'])
def updateuserdetails():
   if request.method =="POST":
        loginid = request.form.get('loginid')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE signup 
        set username=%s,password=%s,email=%s
        where loginid=%s
""", (username,password,email,loginid))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/userdetails')



@app.route('/deleteuserdetails/<int:loginid>', methods = ['POST','GET'])
def deleteuserdetails(loginid):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM signup WHERE loginid=%s", ([loginid]))

    mysql.connection.commit()
    return redirect('/userdetails')







@app.route('/admindetails')
def admindetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from adminlogin")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('admindetails.html', admindetails=rows)







@app.route("/insertadmindetails",methods=["POST","GET"])
def insertadmindetails():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        adminusername = request.form.get('adminusername')
        adminpassword = request.form.get('adminpassword')

        cur.execute("INSERT INTO adminlogin (adminusername,adminpassword) VALUES (%s, %s)",[adminusername,adminpassword])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/admindetails')




@app.route('/updateadmindetails',methods=['POST'])
def updateadmindetails():
   if request.method =="POST":
        adminid = request.form.get('adminid')
        adminusername = request.form.get('adminusername')
        adminpassword = request.form.get('adminpassword')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE adminlogin 
        set adminusername=%s,adminpassword=%s
        where adminid=%s
""", (adminusername,adminpassword,adminid))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/admindetails')



@app.route('/deleteadmindetails/<int:adminid>', methods = ['POST','GET'])
def deleteadmindetails(adminid):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM adminlogin WHERE adminid=%s", ([adminid]))

    mysql.connection.commit()
    return redirect('/admindetails')






@app.route('/batchtimedetails')
def batchtimedetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from batchtime")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('batchtimedetails.html', batchtimedetails=rows)






@app.route('/updatebatchtimedetails',methods=['POST'])
def updatebatchtimedetails():
   if request.method =="POST":
        idbatchtime = request.form.get('idbatchtime')
        userid = request.form.get('userid')
        batchtime = request.form.get('batchtime')
        batchdate = request.form.get('batchdate')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE batchtime 
        set userid=%s,batchtime=%s,batchdate=%s
        where idbatchtime=%s
""", (userid,batchtime,batchdate,idbatchtime))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/batchtimedetails')



@app.route('/deletebatchtimedetails/<int:idbatchtime>', methods = ['POST','GET'])
def deletebatchtimedetails(idbatchtime):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM batchtime WHERE idbatchtime=%s", ([idbatchtime]))

    mysql.connection.commit()
    return redirect('/batchtimedetails')



@app.route('/contactdetails')
def contactdetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from contact")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('contactdetails.html', contactdetails=rows)


#couple batch

@app.route('/coupledetails')
def coupledetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from couple")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('coupledetails.html', coupledetails=rows)



@app.route("/insertcouplebatch",methods=["POST","GET"])
def insertcouplebatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO couple (couplebatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/coupledetails')



@app.route('/updatecouplebatch',methods=['POST'])
def updatecouplebatch():
   if request.method =="POST":
        idcouple = request.form.get('idcouple')
        couplebatchtime = request.form.get('couplebatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE couple 
        set couplebatchtime=%s
        where idcouple=%s
""", (couplebatchtime,idcouple))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/coupledetails')



@app.route('/deletecouplebatch/<int:idcouple>', methods = ['POST','GET'])
def deletecouplebatch(idcouple):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM couple WHERE idcouple=%s", ([idcouple]))

    mysql.connection.commit()
    return redirect('/coupledetails')


#junior batch

@app.route('/juniordetails')
def juniordetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from junior")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('juniordetails.html', juniordetails=rows)



@app.route("/insertjuniorbatch",methods=["POST","GET"])
def insertjuniorbatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO junior (juniorbatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/juniordetails')



@app.route('/updatejuniorbatch',methods=['POST'])
def updatejuniorbatch():
   if request.method =="POST":
        idjunior = request.form.get('idjunior')
        juniorbatchtime = request.form.get('juniorbatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE junior
        set juniorbatchtime=%s
        where idjunior=%s
""", (juniorbatchtime,idjunior))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/juniordetails')



@app.route('/deletejuniorbatch/<int:idjunior>', methods = ['POST','GET'])
def deletejuniorbatch(idjunior):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM junior WHERE idjunior=%s", ([idjunior]))

    mysql.connection.commit()
    return redirect('/juniordetails')



#kids batch

@app.route('/kidsdetails')
def kidsdetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from kids")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('kidsdetails.html', kidsdetails=rows)



@app.route("/insertkidsbatch",methods=["POST","GET"])
def insertkidsbatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO kids (kidsbatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/kidsdetails')



@app.route('/updatekidsbatch',methods=['POST'])
def updatekidsbatch():
   if request.method =="POST":
        idkids = request.form.get('idkids')
        kidsbatchtime = request.form.get('kidsbatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE kids
        set kidsbatchtime=%s
        where idkids=%s
""", (kidsbatchtime,idkids))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/kidsdetails')



@app.route('/deletekidsbatch/<int:idkids>', methods = ['POST','GET'])
def deletekidsbatch(idkids):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM kids WHERE idkids=%s", ([idkids]))

    mysql.connection.commit()
    return redirect('/kidsdetails')



#women batch

@app.route('/womendetails')
def womendetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from women")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('womendetails.html', womendetails=rows)



@app.route("/insertwomenbatch",methods=["POST","GET"])
def insertwomenbatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO women (womenbatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/womendetails')



@app.route('/updatewomenbatch',methods=['POST'])
def updatewomenbatch():
   if request.method =="POST":
        idwomen = request.form.get('idwomen')
        womenbatchtime = request.form.get('womenbatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE women
        set womenbatchtime=%s
        where idwomen=%s
""", (womenbatchtime,idwomen))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/womendetails')



@app.route('/deletewomenbatch/<int:idwomen>', methods = ['POST','GET'])
def deletewomenbatch(idwomen):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM women WHERE idwomen=%s", ([idwomen]))

    mysql.connection.commit()
    return redirect('/womendetails')




#adult batch

@app.route('/adultdetails')
def adultdetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from adult")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('adultdetails.html', adultdetails=rows)



@app.route("/insertadultbatch",methods=["POST","GET"])
def insertadultbatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO adult (adultbatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/adultdetails')



@app.route('/updateadultbatch',methods=['POST'])
def updateadultbatch():
   if request.method =="POST":
        idadult = request.form.get('idadult')
        adultbatchtime = request.form.get('adultbatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE adult
        set adultbatchtime=%s
        where idadult=%s
""", (adultbatchtime,idadult))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/adultdetails')



@app.route('/deleteadultbatch/<int:idadult>', methods = ['POST','GET'])
def deleteadultbatch(idadult):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM adult WHERE idadult=%s", ([idadult]))

    mysql.connection.commit()
    return redirect('/adultdetails')



#fitness batch

@app.route('/fitnessdetails')
def fitnessdetails():
    cursor = mysql.connection.cursor()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("select * from fitness")
    rows = cur.fetchall()

    cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
    # menu = cur.fetchall()

    cur.close()
    return render_template('fitnessdetails.html', fitnessdetails=rows)



@app.route("/insertfitnessbatch",methods=["POST","GET"])
def insertfitnessbatch():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':

        batchtime = request.form.get('batchtime')


        cur.execute("INSERT INTO fitness (fitnessbatchtime) VALUES (%s)",[batchtime])
        mysql.connection.commit()
        cur.close()
        flash('Data Inserted Successfully')
    return redirect('/fitnessdetails')



@app.route('/updatefitnessbatch',methods=['POST'])
def updatefitnessbatch():
   if request.method =="POST":
        idfitness = request.form.get('idfitness')
        fitnessbatchtime = request.form.get('fitnessbatchtime')

        cur =mysql.connection.cursor()
        cur.execute("""
        UPDATE fitness
        set fitnessbatchtime=%s
        where idfitness=%s
""", (fitnessbatchtime,idfitness))

        flash("Data Updated Successfully!!")
        mysql.connection.commit()
        return redirect('/fitnessdetails')



@app.route('/deletefitnessbatch/<int:idfitness>', methods = ['POST','GET'])
def deletefitnessbatch(idfitness):


    flash("Record Deleted Successfully!!")

    cur =mysql.connection.cursor()
    cur.execute("DELETE FROM fitness WHERE idfitness=%s", ([idfitness]))

    mysql.connection.commit()
    return redirect('/fitnessdetails')


@app.route('/loginsector')
def loginsector():
    return render_template('loginsector.html')

#styledetails

# @app.route('/styledetails')
# def styledetails():
#     cursor = mysql.connection.cursor()

#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#     cur.execute("select * from style")
#     rows = cur.fetchall()

#     cursor = mysql.connection.cursor()
#     # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     # cur.execute("SELECT menuid,imagename,url FROM menuframe WHERE unitid=%s", [unitid])
#     # menu = cur.fetchall()

#     cur.close()
#     return render_template('styledetails.html', styledetails=rows)



# @app.route("/insertstyledetails",methods=["POST","GET"])
# def insertstyledetails():
#     cursor = mysql.connection.cursor()
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#     if request.method == 'POST':
#         info = request.form.get('info')
#         file = request.files['image']
#         imagename = secure_filename(file.filename)
#         data = file.read()


#         cur.execute("INSERT INTO style (imagedata,imagename,imageinfo) VALUES (%s,%s,%s)",[data,imagename,info])
#         mysql.connection.commit()
#         cur.close()
#         flash('Data Inserted Successfully')
#     return redirect('/styledetails')



# @app.route('/updatestyledetails',methods=['POST'])
# def updatestyledetails():
#    if request.method =="POST":
#         idstyle = request.form.get('idstyle')
#         stylebatchtime = request.form.get('stylebatchtime')

#         cur =mysql.connection.cursor()
#         cur.execute("""
#         UPDATE style
#         set stylebatchtime=%s
#         where idstyle=%s
# """, (stylebatchtime,idstyle))

#         flash("Data Updated Successfully!!")
#         mysql.connection.commit()
#         return redirect('/styledetails')



# @app.route('/deletestyledetails/<int:idstyle>', methods = ['POST','GET'])
# def deletestyledetails(idstyle):


#     flash("Record Deleted Successfully!!")

#     cur =mysql.connection.cursor()
#     cur.execute("DELETE FROM style WHERE idstyle=%s", ([idstyle]))

#     mysql.connection.commit()
#     return redirect('/styledetails')


if __name__ == '__main__':
    app.run(debug=True)

