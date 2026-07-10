import secrets

secret_key=secrets.token_urlsafe(32) #generating random secret key for jwt
print(secret_key)