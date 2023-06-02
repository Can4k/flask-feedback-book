from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__, static_url_path='/static')


def get_all_posts():
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM POSTS")

    fetched_posts = cursor.fetchall()

    rows = []

    for row in fetched_posts:
        post = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'date': row[3],
            'message': row[4]
        }
        rows.append(post)

    cursor.close()
    conn.close()
    return rows


def insert_post(title, author, message):
    conn = sqlite3.connect('identifier.sqlite')
    cursor = conn.cursor()

    now = datetime.now()
    date = now.strftime("%d.%m.%Y, %H:%M")

    posts.append({
        'title': title,
        'autor': author,
        'message': message,
        'date': date
    })

    cursor.execute("INSERT INTO POSTS (title, author, date, message) VALUES (?, ?, ?, ?)",
                   (title, author, date, message))

    conn.commit()

    cursor.close()
    conn.close()


posts = get_all_posts()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        title, message, author = request.form['title'], request.form['message'], request.form['author']
        insert_post(title, author, message)

    empty_list = not len(posts)
    print(posts, empty_list)
    return render_template('index.html', posts=posts, empty_list=empty_list)


app.run(debug=True)
