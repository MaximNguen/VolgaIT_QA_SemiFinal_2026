"""Тестовые данные для тестов."""
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=length))
    return random_string


valid_registration = [
    ("text", "textAhMoment", "Fodi2006@"),
    ("bruh", "offerPls", "testPass2006@"),
]

invalid_registration = [
    ("text", "textAhMoment", "aodi2006@"),
    ("bruh", "offerPls", "testsass2006@"),
]

valid_login = ("Maxtest", "Fodi2006@")

invalid_login_password = "WrongPass1@"

unknown_login = (f"qa{generate_random_string(12)}", "Fodi2006@")
