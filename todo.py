from flask import Flask, render_template, url_for, request, redirect
import psycopg2
import os

# Set environment variables
os.environ['API_USER'] = 'username'
USER = os.getenv('API_USER')
print(USER)
# Configura i dettagli di connessione
db_params = {
 
}

# Crea una connessione al database
conn = psycopg2.connect(**db_params)

# Crea un cursore per eseguire le query
cur = conn.cursor()
import random
app = Flask(__name__)
todos = []
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        todo_name = request.form['todoName']
        cur_id = random.randint(1, 1000)

        # Esegui una query per inserire un nuovo "To-Do" nel database
        insert_query = "INSERT INTO py_todo_list (id, name, checked) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (cur_id, todo_name, False))
        conn.commit()

    # Esegui una query per ottenere tutti i "To-Do" dal database
    select_query = "SELECT * FROM py_todo_list"
    cur.execute(select_query)
    todosFromDB = cur.fetchall()
    for row in todosFromDB:
        todo = {
          "id": row[0],
          "name": row[1],
          "checked": row[2]
        }
        todos.append(todo)
    print(f"print ${todosFromDB} and todos are {todos}")
    return render_template("index.html", items=todos)

@app.route('/checked/<int:todo_id>', methods=["POST"])

# def checked_todo(todo_id):
#     for todo in todos:
#         if todo['id'] == todo_id:
#              todo['checked'] = not todo['checked']
#              break
#     return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id):
    # Esegui una query per eliminare il "To-Do" dal database
    delete_query = "DELETE FROM py_todo_list WHERE id = %s"
    cur.execute(delete_query, (todo_id,))
    conn.commit()

    # Rimuovi il "To-Do" dall'elenco "todos"
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)

    return redirect(url_for('home'))
# def delete_todo(todo_id):
#     global todos 
#     for todo in todos:
#         if todo['id'] == todo_id:
#             todos.remove(todo)
#     return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)