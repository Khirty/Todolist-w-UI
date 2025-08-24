from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",      # change to your MySQL username
    password="",      # change to your MySQL password
    database="todolist_db"
)
cursor = conn.cursor(dictionary=True)

@app.route("/")
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form["task"]
    cursor.execute("INSERT INTO tasks (text) VALUES (%s)", (task_text,))
    conn.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):
    new_text = request.form["task"]
    cursor.execute("UPDATE tasks SET text=%s WHERE id=%s", (new_text, id))
    conn.commit()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
