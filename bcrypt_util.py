import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid_hashed_pw(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
