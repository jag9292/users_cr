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

@app.route('/users/show/<id>')
def show_user_page(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM users WHERE id=%(id)s;"
    data = {
        "id" : int(id)
    }
    user = mysql.query_db(query, data)
    return render_template('index_show.html', user = user[0])



@app.route('/users/edit/<id>')
def edit(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM users WHERE id=%(id)s;"
    data = {
        "id" : int(id)
    }
    user = mysql.query_db(query, data)
    return render_template('index_edit.html', user = user[0])

@app.route("/edit/<id>", methods=["POST"])
def update(id):
    mysql = connectToMySQL('users')
    query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
    data = {
        "first_name" : request.form['fname'],
        "last_name" : request.form['lname'],
        "email" : request.form['email'],
        "id" : int(id)
    }
    mysql.query_db(query, data)
    return redirect(f'/users/show/{id}')



@app.route('/delete/<id>')
def delete_user(id):
    mysql = connectToMySQL('users')
    query = "DELETE FROM users WHERE id=%(id)s;"
    data = {
        "id" : int(id)
    }
    mysql.query_db(query, data)
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)