from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify, abort
import mysql.connector
import datetime
import random
from flask_login import LoginManager, login_required, current_user
import os

app = Flask(__name__, template_folder='template')
app.secret_key = 'mysecretkey'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="taskmanager"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(405)
@app.errorhandler(404)
def error_handler(error):

    ERROR_IMAGES = [
    "https://media.giphy.com/media/26DNfEyKEiWj4oYyQ/giphy.gif",
    "https://media.giphy.com/media/8L0Pky6C83SzkzU55a/giphy.gif",
    "https://media.giphy.com/media/FYUnDtud95kMKCovAY/giphy.gif",
    "https://media.giphy.com/media/l3V0o1cNQawblEBjy/giphy.gif"
]
    random_image = random.choice(ERROR_IMAGES)
    if 'username' in session:
        return render_template('404.html', random_image=random_image, home_url=url_for('lobby'))
    else:
        return render_template('404.html', random_image=random_image, home_url=url_for('index'))


@app.route('/index', methods=['POST'])
def login():
    username = request.form['username']
    app.logger.info('This is an info message')
    session['username'] = username
    return redirect(url_for("lobby"))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lobby')
def lobby():
    try:
        username = session['username']
    except KeyError:
        return render_template('index.html',error_message="You are not logged in")
    cursor=mydb.cursor()
    cursor.execute('SELECT * FROM task')
    data = cursor.fetchall()
    cursor.close()
    return render_template('lobby.html', username=username, background_image="lobby.jpg", tasks=data)

@app.route('/create_task', methods=['GET','POST'])
def create_task():

    task = request.form.get('task_name')
    desc = request.form.get('task_description')
    username = session['username']
    due = request.form.get('task_due_date')
    status= request.form.get('task_status')
    priority = request.form.get('task_priority')    
    app.logger.info(f'Task: {task}, Description: {desc}, User: {username}, Due: {due}')
    cursor = mydb.cursor()
    cursor.execute('INSERT INTO task (task_name,task_description, task_created_by, task_due_by, task_status, task_priority) VALUES (%s, %s, %s, %s, %s, %s)', (task, desc ,username, due, status, priority))
    mydb.commit()
    cursor.close()
    return redirect(url_for('lobby'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    id = request.form.get('task_id')
    app.logger.info(id)
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM task WHERE task_id = %s', (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('lobby'))

@app.route('/edit_check_task', methods=['POST'])
def edit_check_task():
    id = request.form.get('task_id')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM task WHERE task_id = %s', (id,))
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)
    
@app.route('/edit_task', methods=['POST'])
def edit_task():
    id = request.form.get('task_id')
    task = request.form.get('task_name')
    desc = request.form.get('task_description')
    username = session['username']
    due = request.form.get('task_due_date')
    status= request.form.get('task_status')
    priority = request.form.get('task_priority') 
    app.logger.info(f'Task: {task}, Description: {desc}, User: {username}, task_id: {id}')   
    cursor = mydb.cursor()
    cursor.execute('UPDATE task SET task_name = %s, task_description = %s, task_due_by = %s, task_status = %s, task_priority = %s WHERE task_id = %s', (task, desc, due, status, priority, id))
    mydb.commit()
    cursor.close()
    return redirect(url_for('lobby'))

@app.route('/sort_priority/<order>', methods=['POST'])
def sort_priority(order):
    if order == 'asc':
        query = 'SELECT * FROM task ORDER BY CASE WHEN task_priority = "Urgent" THEN 1 WHEN task_priority = "High" THEN 2 WHEN task_priority = "Normal" THEN 3 WHEN task_priority = "Low" THEN 4 END ASC'   
    elif order == 'dsc':
        query = 'SELECT * FROM task ORDER BY CASE WHEN task_priority = "Urgent" THEN 1 WHEN task_priority = "High" THEN 2 WHEN task_priority = "Normal" THEN 3 WHEN task_priority = "Low" THEN 4 END DESC'  
    else:
        query = 'SELECT * FROM task'
    
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/sort_status/<order>', methods=['POST'])
def sort_status(order):
    if order == 'asc':
        query = 'SELECT * FROM task ORDER BY CASE WHEN task_status = "Not Started" THEN 1 WHEN task_status = "In Progress" THEN 2 WHEN task_status = "Completed" THEN 3 END DESC'   
    elif order == 'dsc':
        query = 'SELECT * FROM task ORDER BY CASE WHEN task_status = "Not Started" THEN 1 WHEN task_status = "In Progress" THEN 2 WHEN task_status = "Completed" THEN 3 END ASC'
    else:
        query = 'SELECT * FROM task'
    
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/sort_due/<order>', methods=['POST'])
def sort_due(order):
    if order == 'asc':
        query = 'SELECT * FROM task ORDER BY task_due_by ASC'   
    elif order == 'dsc':
        query = 'SELECT * FROM task ORDER BY task_due_by DESC'
    else:
        query = 'SELECT * FROM task'
    
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Server running on port 5000")