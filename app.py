from flask import *
import pymysql
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images"

@app.route("/api/signup", methods=["POST"])
def signUp():
    try:
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            
            # create connection to db
            connection = pymysql.connect(host="localhost", user="root", password="", database="ndege_sokogarden")
            # create cursor to handle sql queries
            cursor = connection.cursor()
            # create the sql query
            sql = "insert into users (username1, email, phone, password) values (%s, %s, %s, %s)"
            # data to be save
            data = (username, email, phone, password)
            print(data)
            # execute the sql query
            cursor.execute(sql, data)
            # save the data
            connection.commit()
            # return the response
            return jsonify({"mesage": "Sign up successful"})
    except:
        return jsonify({"mesage": "Sign up unsuccessful. Something went wrong"})

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
    

@app.route("/api/add_product", methods=["POST"])
def addProduct():
    product_name = request.form['product_name']  
    product_description = request.form['product_description']  
    product_category = request.form['product_category']  
    product_cost = request.form['product_cost']  
    product_image = request.files['product_image']

    print(product_name, product_description, product_category, product_cost, product_image)

    # get image name
    image_name = product_image.filename
    print(image_name) 

    # save the image to folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    print(file_path)
    product_image.save(file_path)

    
    # create connection to db
    connection = pymysql.connect(host="localhost", user="root", password="", database="ndege_sokogarden")
    # create cursor to handle sql queries
    cursor = connection.cursor()
    # create the sql query
    sql = "insert into product_details (product_name, product_description, product_category, product_cost, product_image) values (%s, %s, %s, %s, %s)"
    # data to be save
    data = (product_name, product_description, product_category, product_cost, image_name)
    print(data)
    # execute the sql query
    cursor.execute(sql, data)
    # save the data
    connection.commit()
    # return the response
    return jsonify({"mesage": "Product added successful"})


@app.route("/api/get_products")
def getProducts():
    connection = pymysql.connect(host="localhost", user="root", password="", database="ndege_sokogarden")
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # sql query
    sql = "select * from product_details"

    cursor.execute(sql)


    if cursor.rowcount == 0:
        return jsonify({"message": "no products found"})
    else:
        # fetch the products
        products = cursor.fetchall()
        return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)