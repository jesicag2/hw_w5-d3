# HW: Managing a Fitness Center Database

# Task 1: Setting Up the Flask Environment and Database Connection
'''
Create a new Flask project and set up a virtual environment.
Install necessary packages like Flask, Flask-Marshmallow, and MySQL connector.
Establish a connection to your MySQL database.
Create a Member and WorkoutSessions tables to collect data.
'''

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connect_db import connect_db, Error

app = Flask(__name__)

app.json.sort_keys = False

ma = Marshmallow(app)


# Task 2: Implementing CRUD Operations for Members
'''
Create Flask routes to add, retrieve, update, and delete members from the Members table.
Use appropriate HTTP methods: POST for adding, GET for retrieving, PUT for updating, and DELETE for deleting members.
Ensure to handle any errors and return appropriate responses.
'''

class MemberSchema(ma.Schema):
    member_id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    membership_type = fields.String(required=True)

    class Meta:  
        
        fields = ("member_id", "name", "email", "phone", "membership_type")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return "Welcome to our super cool Fitness Tracker, time to get fit!"

@app.route('/members', methods=['GET'])
def get_members(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True) # only for GET dictionary = True
        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members', methods = ['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['email'], member_data['phone'], member_data['membership_type'])

        query = "INSERT INTO Members (name, email, phone, membership_type) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message":"New member added succesfully"}), 201
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

@app.route('/members/<int:id>', methods= ["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['email'], member_data['phone'], member_data['membership_type'], id)

        query = "UPDATE Members SET name = %s, email = %s, phone = %s, membership_type = %s WHERE member_id = %s"

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message":"Member details were succesfully updated!"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=["DELETE"])
def delete_member(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)
        
        query = "SELECT * FROM Members WHERE member_id = %s"

        cursor.execute(query, member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "User does not exist"}), 404
        
        del_query = "DELETE FROM Members where member_id = %s"
        cursor.execute(del_query, member_to_remove)
        conn.commit()

        return jsonify({"message":"Member Removed succesfully"}), 200   

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Task 3: Managing Workout Sessions
'''
Develop routes to schedule, update, and view workout sessions.
'''

class WorkoutSchema(ma.Schema):
    sesh_id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    member_id = fields.Int(required=True)
    workout_type = fields.String(required=True)

    class Meta:  
        
        fields = ("sesh_id", "member_id", "date", "workout_type")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/workouts', methods=['GET'])
def get_workouts(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Workout_sesh"

        cursor.execute(query)

        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workouts', methods = ['POST'])
def add_workout():
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout = (workout_data['date'], workout_data['member_id'], workout_data['workout_type'])

        query = "INSERT INTO Workout_sesh (date, member_id, workout_type) VALUES (%s, %s, %s)"

        cursor.execute(query, new_workout)
        conn.commit()

        return jsonify({"message":"New workout session added succesfully"}), 201
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

@app.route('/workouts/<int:sesh_id>', methods= ["PUT"])
def update_workout(sesh_id):
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_workout = (workout_data['date'], workout_data['member_id'], workout_data['workout_type'], sesh_id)

        query = "UPDATE Workout_sesh SET date = %s, member_id = %s, workout_type = %s WHERE sesh_id = %s"

        cursor.execute(query, updated_workout)
        conn.commit()

        return jsonify({"message":"Workout details were succesfully updated!"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)