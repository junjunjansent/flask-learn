from dotenv import load_dotenv
import os

load_dotenv()

jwt_secret = os.getenv('JWT_SECRET')

import jwt

def jwt_encoder(payload):
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token

def jwt_verifier(token):
    try: 
        decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return decoded_token, None
    except Exception as err:
        return None, str(err)
