import psycopg2.extras
from flask import Flask, Response, jsonify, request
from utils.jwt_util import jwt_encoder, jwt_verifier
from utils.bcrypt_util import hash_password, is_valid_hashed_pw
from utils.db import get_db_connection, get_db_connection1
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/information')
def info():
    return 'Flask is the micro-framework of choice for building Machine Learning API endpoints'

# ------- Param Routing

personnel = {
    "rachel": "Executive Vice President of Managerial Functions",
    "wallace": "Senior Vice President of Managerial Functions",
    "rosie": "Staff Vice President of Managerial Functions",
    "james": "Vice Vice President of Managerial Functions",
    "henri": "Junior Vice President of Managerial Functions"
}

@app.route('/profile/<name>')
def profile(name):
    if name in personnel:
        return f"{personnel.get(name)}"
    else:
        return Response("{'message': 'Name does not have a role.' }", status=201)


# ------- Token trial

user = {
    "id": 1,
    "username": "test",
    "password": 1234    
}                      

@app.route('/token', methods=['GET'])
def sign_token():
    token = jwt_encoder(user)
    # return jsonify({ "message": "You are authorized!"})
    return jsonify(token), 200

@app.route('/token', methods=['POST'])
def verify_token():
    auth_header = request.headers.get('Authorization')

    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header must start with 'Bearer'"}), 400
    
    auth_token = auth_header.split(' ')[1]
    decoded, err = jwt_verifier(auth_token)

    if err:
        return jsonify({"error": err}), 401
    
    return jsonify(decoded), 200


# ------- bcrypt & db trial
@app.route('/db', methods=['GET'])
def get_users():
    connection = get_db_connection()
    # # without cursor_factory=psycopg2.extras.RealDictCursor
    # cursor = connection.cursor()

    # with cursor_factory=psycopg2.extras.RealDictCursor
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute('SELECT * FROM users;')
        data = cursor.fetchall()
        
        # # May need to convert to dictionary
        # colnames = [desc[0] for desc in cursor.description]
        # users = [dict(zip(colnames, row)) for row in data]
        # return jsonify(users)

        return jsonify(data)
    except Exception as err:
        print(err)
        return {"error": "Something went wrong"}, 500
    finally:
        cursor.close()
        connection.close()

@app.route('/bcrypt-sign-up', methods=['POST'])
def sign_up():
    # cannot do .values() because order may not be correct
    username = request.get_json().get('username')
    password = request.get_json().get('password')

    if not username or not password:
        return {"error": "Username & Password required"}, 401

    try: 
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # check username exists
        cursor.execute("SELECT * FROM users WHERE username = %s;", (username, ))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"error": "Username already taken"}, 401
            # close in finally
        
        # start hashing password
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit() # save changes

        # find the last insertion
        cursor.execute("SELECT id, username FROM users WHERE username = %s;", (username,))
        new_user = cursor.fetchone()

        return jsonify({"message": "Sign up route reached.", "data":  new_user}), 201
    except Exception as err:
        connection.rollback()
        print(err)
        return {"error": str(err)}, 401
    finally:
        cursor.close()
        connection.close()


@app.route('/bcrypt-sign-in', methods=['POST'])
def sign_in():
    username = request.get_json().get('username')
    password = request.get_json().get('password')

    if not username or not password:
        return {"error": "Username & Password required"}, 401
    
    try:
        connection, cursor = get_db_connection1()

        # find if user exists
        cursor.execute("SELECT * FROM users WHERE username = %s;", (username, ))
        existing_user = cursor.fetchone()
        print(existing_user)
        if not existing_user:
            return {"error": "User does not exist"}, 401

        # check if password is correct
        obtained_password = existing_user["password"]
        if not is_valid_hashed_pw(password, obtained_password):
            return {"error": "Incorrect password"}, 401

        # create token
        user_data = dict(existing_user) # best practice
        user_data.pop("password", None)
        token = jwt_encoder(user_data)

        return jsonify({"message": "Sign In route reached.", "data": {"token": token}}), 201
    except Exception as err:
        connection.rollback()
        print(err)
        return {"error": str(err)}, 401
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
