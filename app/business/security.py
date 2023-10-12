import bcrypt


def encrypt(s: str):
    encrypted = bcrypt.hashpw(s.encode(), bcrypt.gensalt())
    return encrypted.decode()


def check_password(unencrypted_password: str, encrypted_password: str):
    return bcrypt.checkpw(unencrypted_password.encode(), encrypted_password.encode())
