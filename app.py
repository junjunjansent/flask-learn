from flask import Flask, Response, jsonify, request
from jwt_util import jwt_encoder, jwt_verifier
from bcrypt_util import hash_password, is_valid_hashed_pw
from db_util import get_db_connection

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
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM users;')
        data = cursor.fetchall()
        
        # # May need to convert to dictionary
        # colnames = [desc[0] for desc in cursor.description]
        # users = [dict(zip(colnames, row)) for row in data]
        # return jsonify(users)

        return jsonify(data)
    except Exception as e:
        print(e)
        return {"error": "Something went wrong"}, 500
    finally:
        cursor.close()
        connection.close()

@app.route('/bcrypt-create', methods=['POST'])
def sign_up():
    return jsonify({"message": "Sign up route reached."})


if __name__ == '__main__':
    app.run(debug=True)
