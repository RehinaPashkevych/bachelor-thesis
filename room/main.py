from datetime import datetime
from flask_restx import Resource
from swagger_config import api, token_parser, token_model
from flask import Flask, render_template, request, jsonify
import random
import string
import mysql.connector

app = Flask(__name__)
api.init_app(app)  # init object Api
api = api.namespace('', description='HTTP Operations related to tokens')

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


@app.route('/token/<int:id>', methods=['GET', 'POST', 'DELETE'])
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


@api.route('/api/token/<int:id>')
class TokenResource(Resource):
    def get(self, id):
        token, password, creation_time = retrieve_token_info(id)
        if token is not None:
            # Convert date to string before returning response
            creation_time_str = creation_time.strftime("%Y-%m-%d %H:%M:%S") if creation_time else None
            return {'id': id, 'token': token, 'password': password, 'creation_time': creation_time_str}
        else:
            api.abort(404, f"Row with ID {id} not found")

    @api.expect(token_parser)
    def post(self, id):
        args = token_parser.parse_args()
        new_token = args['token']
        new_password = args['password']
        if update_token_info(id, new_token, new_password):
            return f"Information for ID {id} has been updated."
        else:
            api.abort(404, f"Row with ID {id} not found")

    def delete(self, id):
        if delete_token(id):
            return f"Row with ID {id} has been deleted."
        else:
            api.abort(404, f"Row with ID {id} not found")


@api.route('/api/tokens')
class TokenList(Resource):
    @api.doc(responses={200: 'OK'})
    def get(self):
        try:
            conn, cursor = connect_to_database()

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

            # Fetch the results after executing the query
            tokens = cursor.fetchall()

            # Convert the creation_time to ISO format for each token
            results = [{'id': token['id'],
                        'token': token['token'],
                        'password': token['password'],
                        'creation_time': token['creation_time'].isoformat()} for token in tokens]

            close_database_connection(cursor, conn)
            return results, 200

        except mysql.connector.Error as e:
            print("Error:", e)
            return {"error": "An error occurred while fetching token data."}, 500



@app.route('/tokens', methods=['GET'])
def display_filtered_tokens():
    try:
        conn, cursor = connect_to_database()

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
        close_database_connection(cursor, conn)

    return "An error occurred while fetching token data."


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


@api.route('/api/get-data/<string:token>')
class TokenResource(Resource):
    @api.marshal_with(token_model)
    def get(self, token):
        data = retrieve_token_info_by_token(token)
        if data:
            response_data = {
                'token': data[0],  # Assuming data[0] contains the token
                'password': data[1]  # Assuming data[1] contains the password
            }
            return response_data
        else:
            api.abort(404, 'Token not found')


def retrieve_token_info_by_token(token):
    try:
        conn, cursor = connect_to_database()

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
        close_database_connection(cursor, conn)

    return None, None  # Return None if the row is not found or an error occurs


def generate_token():
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    return token


# Function to insert the token and password into the MySQL database
def insert_data_into_db(token, password):
    try:
        conn, cursor = connect_to_database()
        insert_query = "INSERT INTO `room-db` (token, password) VALUES (%s, %s)"  # Use backticks for the table name
        cursor.execute(insert_query, (token, password))
        conn.commit()
        close_database_connection(cursor, conn)
    except mysql.connector.Error as e:
        print("Error:", e)


def retrieve_token_info(id):
    try:
        conn, cursor = connect_to_database()

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
        close_database_connection(cursor, conn)

    return None, None, None  # Return None if the row is not found or an error occurs


def delete_token(id):
    try:
        conn, cursor = connect_to_database()

        # Execute a DELETE query to remove the row with the specified id
        cursor.execute("DELETE FROM `room-db` WHERE id = %s", (id,))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            close_database_connection(cursor, conn)
            return True
        else:
            # No rows were affected, indicating the ID was not found
            close_database_connection(cursor, conn)
            return False

    except mysql.connector.Error as e:
        print("Error:", e)
        return False


def retrieve_all_tokens():
    try:
        conn, cursor = connect_to_database()

        # Query the database to retrieve all data
        cursor.execute("SELECT id, token, password, creation_time FROM `room-db`")
        data = cursor.fetchall()

        return data

    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        close_database_connection(cursor, conn)

    return []  # Return an empty list if an error occurs or no data is found


# Function to update the password for a given token ID
def update_token_info(id, new_token, new_password, new_time=None):
    try:
        conn, cursor = connect_to_database()

        # Determine the new creation time
        if new_time is None:
            new_time = datetime.now()

        # Execute an UPDATE query to change the token, password, and time for the specified ID
        cursor.execute("UPDATE `room-db` SET token = %s, password = %s, creation_time = %s WHERE id = %s",
                       (new_token, new_password, new_time, id))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            close_database_connection(cursor, conn)
            return True
        else:
            # No rows were affected, indicating the ID was not found
            close_database_connection(cursor, conn)
            return False

    except mysql.connector.Error as e:
        print("Error:", e)
        return False


def connect_to_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    return conn, cursor


def close_database_connection(cursor, conn):
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
