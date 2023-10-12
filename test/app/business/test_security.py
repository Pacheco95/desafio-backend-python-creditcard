from app.business.security import encrypt, check_password


def test_encrypt_salt_uses_12_rounds():
    pwd = "some-ultra-secret-password"
    assert check_password(pwd, encrypt(pwd))
