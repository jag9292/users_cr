from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'hey'


@app.route("/users")
def users():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    # print(users)
    return render_template("index.html", all_users = users)


@app.route('/users/new')
def show():
    return render_template('index_new.html')

@app.route('/users', methods=['POST'])
def add_user():
    print('test')
    mysql = connectToMySQL('users')
    print(request.form)
    query = "INSERT INTO users (first_name, last_name, email) VALUES (%(fname)s, %(lname)s, %(email)s);"
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)