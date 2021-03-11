import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS





def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Register_tab (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT, password TEXT, comment TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS blog_content (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, image TEXT)')

    print("Register_tab table created successfully")
    conn.close()


init_sqlite_db()
app = Flask(__name__)
CORS(app)

def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/add-new/', methods=['POST'])
def add_new_record():

    msg = None
    try:
        post_data = request.get_json()
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        email = post_data['email']
        password = post_data['password']
        comment = post_data['comment']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Register_tab (firstname, lastname, email, password, comment) VALUES (?, ?, ?, ?, ?)"
                        ,(firstname, lastname, email, password,comment))
            con.commit()
            msg = firstname + " was successfully added to the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)

    finally:
        con.close()
        return jsonify(msg)







@app.route('/show-sub/', methods=["GET"])
def show_sub():
    records =[]
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Register_tab")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
    return jsonify(records)


def create_blog_table():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Blog (id INTEGER PRIMARY KEY AUTOINCREMENT, comments TEXT)')
    print("Blog table created successfully")


create_blog_table()


@app.route('/comment/', methods=['POST'])
def comments():

    msg = None
    try:
        post_data = request.get_json()
        comments = post_data['comments']
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Blog (comments) VALUES (?)", (comments,))
            con.commit()
            msg = comments + " was successfully added to the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)

    finally:
        con.close()
        return jsonify(msg)

@app.route('/show-comments/', methods=["GET"])
def show_comments():
    records={}
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Register_tab")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
    return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)



@app.route('/delete/<int:view_id>/', methods=["DELETE"])
def delete(view_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE id=" + str(view_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)





if __name__=='main__':
    app.run(debug=True)
