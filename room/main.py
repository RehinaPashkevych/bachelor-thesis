from datetime import datetime

from flask import Flask, render_template, request, jsonify
import random
import string
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'test'
}


# Function to generate a random 5-character token

@app.route('/generate-token', methods=['GET', 'POST'])
def generate_and_insert_token():
    password = ""  # Initialize the password variable
    token = ""

    if request.method == 'POST':
        password = request.form.get('password')  # Retrieve the password from the form
        token = generate_token()
        insert_data_into_db(token, password)

    return render_template('index.html', token=token, password=password)


@app.route('/token/<int:id>', methods=['GET', 'POST', 'DELETE'])  # ADD PUT METHOD
def display_or_delete_or_update_token_info(id):
    if request.method == 'GET':
        # Retrieve and display token information
        token, password, creation_time = retrieve_token_info(id)
        if token is not None:
            return render_template('token_info.html', id=id, token=token, password=password,
                                   creation_time=creation_time)
        else:
            return "Row with ID {} not found.".format(id), 404

    elif request.method == 'POST':
        # Update the password and the token for the specified token ID
        new_token = request.form.get('token')
        new_password = request.form.get('password')
        if update_token_info(id, new_token, new_password):
            return "Information for ID {} has been updated.".format(id)
        else:
            return "Row with ID {} not found.".format(id), 404

    elif request.method == 'DELETE':
        # Delete the row with the specified id
        if delete_token(id):
            return "Row with ID {} has been deleted.".format(id)
        else:
            return "Row with ID {} not found.".format(id), 404


@app.route('/tokens', methods=['GET'])
def display_filtered_tokens():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Default query to retrieve all data
        query = "SELECT id, token, password, creation_time FROM `room-db`"

        # Check if filter_by and search_value parameters are provided
        filter_by = request.args.get('filter_by')
        search_value = request.args.get('search_value')

        # If both filter_by and search_value are provided, add a WHERE clause to the query
        if filter_by and search_value:
            query += f" WHERE `{filter_by}` LIKE '%{search_value}%'"

        # Execute the query
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template('tokens.html', data=data)

    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

    return "An error occurred while fetching token data."


"""
@app.route('/get-token-data-id/<int:id>', methods=['GET'])
def get_token_data(id):
    data = retrieve_token_info(id)
    if data:
        return jsonify(data)  # Return the data as JSON
    else:
        return jsonify({'error': 'Token not found'}), 404
"""

@app.route('/get-data/<string:token>', methods=['GET'])
def get_token_data(token):
    data = retrieve_token_info_by_token(token)
    if data:
        response_data = {
            'token': data[0],  # Assuming data[0] contains the token
            'password': data[1]  # Assuming data[1] contains the password
        }
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Token not found'}), 404

def retrieve_token_info_by_token(token):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query the database to retrieve the token, password, and creation_time for the specified token
        cursor.execute("SELECT token, password FROM `room-db` WHERE token = %s", (token,))
        row = cursor.fetchone()

        if row:
            token = row['token']
            password = row['password']
            return token, password

    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

    return None, None  # Return None if the row is not found or an error occurs

def generate_token():
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    return token


# Function to insert the token and password into the MySQL database
def insert_data_into_db(token, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO `room-db` (token, password) VALUES (%s, %s)"  # Use backticks for the table name
        cursor.execute(insert_query, (token, password))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Error:", e)


def retrieve_token_info(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query the database to retrieve the token, password, and creation_time for the specified id
        cursor.execute("SELECT token, password, creation_time FROM `room-db` WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row:
            token = row['token']
            password = row['password']
            creation_time = row['creation_time']
            return token, password, creation_time

    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

    return None, None, None  # Return None if the row is not found or an error occurs


def delete_token(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute a DELETE query to remove the row with the specified id
        cursor.execute("DELETE FROM `room-db` WHERE id = %s", (id,))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            # No rows were affected, indicating the ID was not found
            cursor.close()
            conn.close()
            return False

    except mysql.connector.Error as e:
        print("Error:", e)
        return False


def retrieve_all_tokens():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query the database to retrieve all data
        cursor.execute("SELECT id, token, password, creation_time FROM `room-db`")
        data = cursor.fetchall()

        return data

    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

    return []  # Return an empty list if an error occurs or no data is found

# Function to update the password for a given token ID
def update_token_info(id, new_token, new_password, new_time=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Determine the new creation time
        if new_time is None:
            new_time = datetime.now()

        # Execute an UPDATE query to change the token, password, and time for the specified ID
        cursor.execute("UPDATE `room-db` SET token = %s, password = %s, creation_time = %s WHERE id = %s", (new_token, new_password, new_time, id))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            # No rows were affected, indicating the ID was not found
            cursor.close()
            conn.close()
            return False

    except mysql.connector.Error as e:
        print("Error:", e)
        return False

if __name__ == '__main__':
    app.run(debug=True)
