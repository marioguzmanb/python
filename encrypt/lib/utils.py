from cryptography.fernet import Fernet
import pandas as pd

def generate_key():
    return Fernet.generate_key()

def encrypt(text, key):
    fernet_token = Fernet(key)
    return fernet_token.encrypt(text.encode()).decode()

def decrypt(text, key):
    fernet_token = Fernet(key)
    return fernet_token.decrypt(text.encode()).decode()

def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")