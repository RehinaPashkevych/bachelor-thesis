from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'test-2'
}

# Define the URL of the first microservice
first_microservice_url = 'http://localhost:5000'


def get_json(response):
    try:
        return response.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return None


@app.route('/register-to-room', methods=['GET', 'POST'])
def register_to_room():
    if request.method == 'POST':
        # Get form data
        name, surname, group, subject, token, password = get_form_data()

        # Send a request to the first microservice to validate the token and password
        validation_response = validate_token_and_password(token, password)

        if validation_response:
            # Token and password are valid, insert student data into the database
            insert_data_into_db(name, surname, group, subject, token, password)
            return "Registration successful"
        else:
            return "Invalid token or password"

    return render_template('index.html')


@app.route('/students', methods=['GET'])
def display_students():
    try:
        conn, cursor = connect_to_database()

        # Get parameters from the request
        sort_by = request.args.get('sort_by', default='id')
        filter_token = request.args.get('token', default=None)
        filter_by = request.args.get('filter_by', default=None)
        search_value = request.args.get('search_value', default=None)

        # Check if the column specified in filter_by exists in the table
        valid_columns = ['name', 'surname', 'group', 'subject', 'token', 'password']
        if filter_by and filter_by not in valid_columns:
            filter_by = None  # Ignoruj nieprawidłową wartość filter_by

        # Build an SQL query including parameters
        query = "SELECT * FROM `students-bd`"

        if filter_token:
            query += f" WHERE `token` = '{filter_token}'"

        if filter_by and search_value:
            # Add a condition to search on specific columns
            if 'WHERE' not in query:
                query += " WHERE"
            else:
                query += " AND"
            query += f" `{filter_by}` LIKE '%{search_value}%'"

        query += f" ORDER BY {sort_by}"

        # Execute the SQL query
        cursor.execute(query)
        students = cursor.fetchall()

        return render_template('students.html', students=students)
    except mysql.connector.Error as e:
        print("Error:", e)
        return "An error occurred while fetching student data."
    finally:
        close_database_connection(cursor, conn)


@app.route('/student/<int:id>', methods=['GET', 'POST', 'DELETE'])
def retrieve_or_delete_student(id):
    if request.method == 'GET':
        # Retrieve and display student information by ID
        student = retrieve_student_info_by_id(id)
        if student:
            return render_template('student_info.html', student=student)
        else:
            return "Student with ID {} not found.".format(id), 404

    if request.method == 'POST':
        # Update the student by ID
        try:
            name, surname, group, subject, token, password = get_form_data()

            insert_data_into_db(name, surname, group, subject, token, password, id)
            return "Student updated successfully"
        except mysql.connector.Error as e:
            print("Error:", e)
            return "An error occurred while updating the student."

    if request.method == 'DELETE':
        # Delete the student by ID
        try:
            conn, cursor = connect_to_database()
            cursor.execute("DELETE FROM `students-bd` WHERE id = %s", (id,))
            conn.commit()
            close_database_connection(cursor, conn)
            return "Student deleted successfully"
        except mysql.connector.Error as e:
            print("Error:", e)
            return "An error occurred while deleting the student."


def retrieve_student_info_by_id(id):
    try:
        conn, cursor = connect_to_database()
        cursor.execute("SELECT * FROM `students-bd` WHERE id = %s", (id,))
        student = cursor.fetchone()
        return student
    except mysql.connector.Error as e:
        print("Error:", e)
        return None
    finally:
        close_database_connection(cursor, conn)


def validate_token_and_password(token, password):
    try:
        response = requests.get(f'{first_microservice_url}/get-data/{token}')
        if response.status_code == 200:
            data = get_json(response)
            if data.get('token') and (data.get('password') == password or password is None):
                return True
        return False
    except Exception as e:
        print("Error:", e)
        return False


def insert_data_into_db(name, surname, group, subject, token, password, student_id=None):
    try:
        if all((name, surname, group, subject, token)):
            conn, cursor = connect_to_database()

            # Check if the student with the given ID already exists
            if student_id is not None and student_id != 0:
                cursor.execute("SELECT COUNT(*) FROM `students-bd` WHERE id = %s", (student_id,))
                count = cursor.fetchone()[0]

                if count > 0:
                    raise ValueError(f"Error: Student with ID {student_id} already exists")

            if student_id is not None and student_id != 0:
                # If id is provided and not zero, include it in the INSERT query
                insert_query = """
                    INSERT INTO `students-bd` (`id`, `name`, `surname`, `group`, `subject`, `token`, `password`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (student_id, name, surname, group, subject, token, password))
            else:
                # If id is not provided or is zero, let the database generate it automatically
                insert_query = """
                    INSERT INTO `students-bd` (`name`, `surname`, `group`, `subject`, `token`, `password`)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, surname, group, subject, token, password))

            conn.commit()
            close_database_connection(cursor, conn)
        else:
            print("Error: All fields are required")
    except mysql.connector.Error as e:
        print("Error:", e)


def get_form_data():
    return (
        request.form.get('name'),
        request.form.get('surname'),
        request.form.get('group'),
        request.form.get('subject'),
        request.form.get('token'),
        request.form.get('password')
    )


def connect_to_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    return conn, cursor


def close_database_connection(cursor, conn):
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
