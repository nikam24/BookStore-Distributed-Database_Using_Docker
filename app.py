from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'site1',
    'user': 'root',
    'password': 'pratham',
    'database': 'Books'
}

# Site configurations
site_configs = {
    'S1': {
        'host': 'site1',
        'user': 'root',
        'password': 'pratham',
        'database': 'Books'
    },
    'S2': {
        'host': 'site2',
        'user': 'root',
        'password': 'pratham',
        'database': 'Books'
    },
}


def determine_site_by_zip(zip_code):
    if zip_code <= 25000:
        return 'S1'
    elif 25001 <= zip_code <= 50000:
        return 'S2'
    elif 50001 <= zip_code <= 75000:
        return 'S3'
    else:
        return 'S4'

# Initialize db_connection outside the try block
db_connection = None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_bookstore', methods=['POST'])
def add_bookstore():
    print("Inside add_bookstore")
    print(request.form)	
    store = request.form['storeNo']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    inventoryValue = request.form['inventoryValue']

    query = "INSERT INTO Bookstores (storeNo, city, state, zip, inventoryValue) VALUES (%s, %s, %s, %s, %s);"
    values = (store, city, state, zip, inventoryValue)

    print("Before try")
    try:
        print("Inside try")
        cursor = db_connection.cursor()
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()
        print("After cursor close")
        alert = "Bookstore added successfully!"
    except Exception as e:
        alert = f"Error adding bookstore: {str(e)}"
        print("Inside except")
    finally:
        print("Inside finally")
        return render_template('index.html', alert=alert)

@app.route('/store/<int:zip_code>')
def get_books_by_zip(zip_code):
    try:
        # Determine the site based on the zip code range
        site = determine_site_by_zip(zip_code)

        # Connect to the appropriate site's database
        db_connection = mysql.connector.connect(**site_configs[site])
        cursor = db_connection.cursor()

        # Execute SQL query to retrieve books information
        query = f"SELECT * FROM Books;"
        cursor.execute(query)
        books = cursor.fetchall()

        cursor.close()
        db_connection.close()

        # Return the retrieved books information
        return render_template('books.html', books=books)
    except Exception as e:
        return f"Error retrieving books information: {str(e)}"

# @app.route('/test_db')
# def test_db():
#     try:
#         cursor = db_connection.cursor()
#         cursor.execute('SELECT 1')
#         result = cursor.fetchone()
#         cursor.close()
#         db_connection.commit()  # Commit any pending transactions
#         return f"Database connection and query successful: {result[0]}"
#     except Exception as e:
#         return f"Error connecting to database: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
