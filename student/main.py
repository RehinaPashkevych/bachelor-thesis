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
        name = request.form.get('name')
        surname = request.form.get('surname')
        group = request.form.get('group')
        subject = request.form.get('subject')
        token = request.form.get('token')
        password = request.form.get('password')

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
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Pobierz parametry z żądania
        sort_by = request.args.get('sort_by', default='id')
        filter_token = request.args.get('token', default=None)
        filter_by = request.args.get('filter_by', default=None)
        search_value = request.args.get('search_value', default=None)

        # Sprawdź, czy kolumna wskazana w filter_by istnieje w tabeli
        valid_columns = ['name', 'surname', 'group', 'subject', 'token', 'password']
        if filter_by not in valid_columns:
            return "Invalid filter_by parameter.", 400

        # Buduj zapytanie SQL z uwzględnieniem parametrów
        query = "SELECT * FROM `students-bd`"

        if filter_token:
            query += f" WHERE `token` = '{filter_token}'"

        if filter_by and search_value:
            # Dodaj warunek do wyszukiwania w określonych kolumnach
            if 'WHERE' not in query:
                query += " WHERE"
            else:
                query += " AND"
            query += f" `{filter_by}` LIKE '%{search_value}%'"

        query += f" ORDER BY {sort_by}"

        # Wykonaj zapytanie SQL
        cursor.execute(query)
        students = cursor.fetchall()

        return render_template('students.html', students=students)
    except mysql.connector.Error as e:
        print("Error:", e)
        return "An error occurred while fetching student data."
    finally:
        cursor.close()
        conn.close()


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
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Assuming you have form data for updating student details
            name = request.form.get('name')
            surname = request.form.get('surname')
            group = request.form.get('group')
            subject = request.form.get('subject')
            token = request.form.get('token')
            password = request.form.get('password')

            insert_data_into_db(name, surname, group, subject, token, password, id)
            return "Student updated successfully"
        except mysql.connector.Error as e:
            print("Error:", e)
            return "An error occurred while updating the student."

    if request.method == 'DELETE':
        # Delete the student by ID
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `students-bd` WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return "Student deleted successfully"
        except mysql.connector.Error as e:
            print("Error:", e)
            return "An error occurred while deleting the student."


def retrieve_student_info_by_id(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `students-bd` WHERE id = %s", (id,))
        student = cursor.fetchone()
        return student
    except mysql.connector.Error as e:
        print("Error:", e)
        return None


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
        if name and surname and group and subject and token :
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

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
            cursor.close()
            conn.close()
        else:
            print("Error: All fields are required")
    except mysql.connector.Error as e:
        print("Error:", e)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
