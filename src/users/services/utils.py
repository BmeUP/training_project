import hashlib
import re

from settings import settings

def validate_phone(phone: str):
    regex = re.compile("(^8|7|\+7)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))")
    return re.fullmatch(regex, phone)

def validate_email(email: str):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)

def hash_password(raw_password):
    hashed_password = hashlib.sha512(f"{raw_password}+{settings.salt}".encode("utf-8")).hexdigest()
    return hashed_password

def check_passwords(raw_password, db_hashed_password):
    hashed_password = hashlib.sha512(f"{raw_password}+{settings.salt}".encode("utf-8")).hexdigest()
    return hashed_password == db_hashed_password