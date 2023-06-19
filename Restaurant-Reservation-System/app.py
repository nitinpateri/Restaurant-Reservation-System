#importing modules
from flask import Flask, render_template, request, redirect
import smtplib
from random import randint


app = Flask(__name__)

#Database connection
import pymongo
client = pymongo.MongoClient(
    "mongodb+srv://Nitin:admin-123@cluster0.lwfqf.mongodb.net/?retryWrites=true&w=majority"
)


#Index Page
@app.route('/')
def index():
    mydb=client['restaurant-reservation-system']
    mycol = mydb['restaurants-info']
    restaurants_info=mycol.find()
    data=[]
    for i in restaurants_info:
        if type(i["City"]) is str:
            data.append(i)
    return render_template('index.html',data=data)
    
#City Page
@app.route('/<city>/City')
def City(city):
    data=[]
    temp=[]
    mydb=client['restaurant-reservation-system']
    mycol = mydb['restaurants-info']
    restaurants_info=mycol.find()
    for i in restaurants_info:
        temp.append(i)
    data.append(temp)
    data.append(city)
    return render_template('city.html',data=data)

#Restaurant Page
@app.route('/<city>/<restaurant>/')
def rest(city,restaurant):
    data=[]
    temp=[]
    mydb=client['restaurant-reservation-system']
    mycol = mydb['restaurants-info']
    restaurants_info=mycol.find()
    temp1=''
    for i in restaurants_info:
        if type(i["City"]) is str:
            temp.append(i)
        else:
            temp1=i
    data.append(temp)
    data.append(city)
    data.append(restaurant)
    data.append(temp1)
    return render_template('restaurant.html',data=data)

#Mail Verification
@app.route("/otp",methods=['POST', "GET"])
def otp(): 
    mail ="noreply.rrs.project@gmail.com"
    password="blevhigipxklthds"
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=mail,password=password)
    if (request.method=="GET"):
        global otp1
        otp1=randint(1111,9999)
        mail_content ="Subject: Email Verification\n\nYour OTP of verifying the RRS is "+str(otp1)
        connection.sendmail(from_addr=mail, to_addrs=email,msg=mail_content)
        return render_template('otp.html')
    if request.method=="POST":
        entered=request.form['otp']
        if entered == str(otp1):
            mail_content ="Subject: Booking Details\n\nThank you for using our sevrvice.Please find the Booking Details below:-\n\n <h1>Name:"+name+"<\h1>\nEmail id:"+email+"\nRESTAUTANT NAME:"+r_name+"Branch"+branch+"\nTotal no. of people:"+count+"\nTime:"+time+"\nDate:"+date
            connection.sendmail(from_addr=mail, to_addrs=email,msg=mail_content)
            return render_template('success.html')
        else:
            return render_template('Failed.html')
        

#Adding details
@app.route("/booking-details", methods=['POST', 'GET'])
def booking_details():
    if request.method == 'POST':
        global name,email,r_name,date,time,r_name,count,branch
        name=request.form['name']
        email =request.form['mail']
        r_name=request.form['r_name']
        count=request.form['members']
        date=request.form['date']
        time=request.form['time']
        branch = request.form["branch"]
        return redirect("/otp")
    

#Adding Restaurants
@app.route("/add-restaurant")
def add_restaurant():
    data=["Hyderabad","Chennai","Bangalore","Visakhapatnam"]
    return render_template("add-restaurant.html",data=data)    

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        open  = request.form['open']
        close = request.form['close']
        Timings =open+" to "+ close
        restaurant={
            "Name":request.form["name"],
            "City":request.form["city"],
            "Cuisine": request.form['cuisine'],
            "Pic": request.form['pic'],
            "Timings" :Timings
        }
        mydb=client['restaurant-reservation-system']
        mycol = mydb['restaurants-info']
        mycol.insert_one(restaurant)
        return render_template("r-success.html")

if __name__=="__main__":
    app.run(host='0.0.0.0', port='8000', debug='True')
    