from flask import Flask, render_template , redirect , request , url_for
from flask_mysqldb import MySQL
import mysql.connector
import requests

app = Flask(__name__)
#buildings=[]
conn = mysql.connector.connect(user='root',password='123456',host='localhost',database='grexter')
mycursor = conn.cursor()
#mycursor.execute("CREATE DATABASE grexter")
#mycursor.execute("USE grexter")
#mycursor.close()
#mycursor = conn.cursor()
#mycursor.execute("USE grexter")
#mycursor.execute("CREATE TABLE buildings( id INT(11) AUTO_INCREMENT PRIMARY KEY , name VARCHAR(100) , address VARCHAR(100) , landmarks VARCHAR(100))")
mycursor.close()
@app.route('/')
def index():
    return render_template('index.html')

#adding buildings
@app.route('/add_building',methods=['GET','POST'])
def add_building():

    if request.method == 'POST':
        name = request.form['name']
        name1 = name.lower()
        address = request.form['address']
        landmarks = request.form['landmarks']
        curr= conn.cursor()
        curr.execute("INSERT INTO buildings(name , address , landmarks) VALUES(%s , %s , %s)" , (name1 , address , landmarks))
        conn.commit()
        #print (buildings)
        curr.close()
        return redirect(url_for('add_rooms'))

    return render_template("add_building.html")

#adding rooms
@app.route('/add_rooms',methods=['GET','POST'])
def add_rooms():
    if request.method == 'POST':
        name = request.form['name']
        print (name)
        name1 = name.lower()
        flat = request.form['flat']
        square = request.form['square']
        rent = request.form['rent']
        Type = request.form['Type']
        bathrooms = request.form['bathrooms']
        maintanence = request.form['maintanence']
        electricity = request.form['electricity']

        if maintanence == "yes":
            maintanence = 1
        else:
            maintanence = 0

        curr = conn.cursor(buffered = True)
        #result = curr.execute("SELECT * FROM buildings WHERE name = %s" , [name])

        curr.execute("SELECT * FROM buildings")
        data = curr.fetchall()
        print (data)
        count=0
        for i in range(len(data)):
            if data[i][1] == name1:
                b_id = data[i][0]
                count+=1
        if count == 0:
            return render_template("add_building.html")
        print (b_id)

        curr = conn.cursor()
        curr.execute("INSERT INTO rooms(build_id, flat_no,square_area ,rent ,type ,No_of_Bathrooms , maintanence,electricity ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(b_id,flat,square,rent,Type,bathrooms,maintanence,electricity))
        conn.commit()
        curr.close()
        return redirect(url_for("index"))


    return render_template("add_rooms.html")
if(__name__ == "__main__"):
    app.run(debug=True)
