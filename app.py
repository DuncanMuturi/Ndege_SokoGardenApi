from flask import *
import pymysql
# import pymysql.cursors

app = Flask(__name__)

@app.route("/api/signup", methods=["POST"])
def signUp():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    
    # create connection to db
    connection = pymysql.connect(host="localhost", user="root", password="", database="ndege_sokogarden")
    # create cursor to handle sql queries
    cursor = connection.cursor()
    # create the sql query
    sql = "insert into users (username, email, phone, password) values (%s, %s, %s, %s)"
    # data to be save
    data = (username, email, phone, password)
    print(data)
    # execute the sql query
    cursor.execute(sql, data)
    # save the data
    connection.commit()
    # return the response
    return jsonify({"mesage": "Sign up successful"})


# Sign in route
@app.route("/api/signin", methods=["POST"])
def signIn():
    email = request.form["email"]
    password = request.form["password"]
    print(email, password)
    # create connection to db
    connection = pymysql.connect(host="localhost", user="root", password="", database="ndege_sokogarden")
    # create cursor to handle sql queries
    # cursor = connection.cursor()

    # cursor to fetch data as key - vaslue pair
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # create the sql query to execute
    sql = "select user_id, username, email, phone from users where email = %s and password =%s"
    # data to execute the query
    data = (email, password)

    # execute the query
    cursor.execute(sql, data)

    # check resulting rows
    if cursor.rowcount == 0:
        return jsonify({"message": "Invalid credentials"})
    else:
        # get the user data
        user = cursor.fetchone()
        return jsonify({"message": "login succesfull", "user": user})
    



if __name__ == "__main__":
    app.run(debug=True)