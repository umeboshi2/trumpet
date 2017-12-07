import bcrypt


def encrypt_password(password):
    if type(password) is str:
        password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode()


def password_matches(user, password):
    hashed = user.password
    if type(hashed) is str:
        hashed = hashed.encode()
    if type(password) is str:
        password = password.encode()
    return bcrypt.checkpw(password, hashed)
