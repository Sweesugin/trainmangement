from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'train'

# MySQL Configuration for the Train Management System
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'train_db2'  # Database should be for train management
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')  # You can create your index page here

@app.route('/train')
def train():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM train_details")  # Fetch all train details
    train_info = cur.fetchall()
    cur.close()
    return render_template('trains.html', trains=train_info)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    search_term = ''
    if request.method == "POST":
        search_term = request.form['train_number']  # Search by Train Number
        cur = mysql.connection.cursor()
        query = "SELECT * FROM train_details WHERE train_number LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)  # Fetching one matching result
        cur.close()
        return render_template('trains.html', trains=search_results)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        train_number = request.form['train_number']
        train_name = request.form['train_name']
        origin = request.form['origin']
        destination = request.form['destination']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO train_details (train_number, train_name, origin, destination) VALUES (%s, %s, %s, %s)",
                    (train_number, train_name, origin, destination))
        mysql.connection.commit()
        return redirect(url_for('train'))

@app.route('/delete/<string:train_number>', methods=['GET'])
def delete(train_number):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM train_details WHERE train_number = %s", (train_number,))
    mysql.connection.commit()
    return redirect(url_for('train'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        # Fetch form data
        train_number = request.form['train_number']
        train_name = request.form['train_name']
        origin = request.form['origin']
        destination = request.form['destination']

        # Corrected SQL query with proper syntax
        cur = mysql.connection.cursor()
        query = """
            UPDATE train_details 
            SET train_name = %s, origin = %s, destination = %s 
            WHERE train_number = %s
        """
        cur.execute(query, (train_name, origin, destination, train_number))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('train'))

if __name__ == "__main__":
    app.run(debug=True)
