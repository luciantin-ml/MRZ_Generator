from mrz.generator.td3 import TD3CodeGenerator
from mrz.checker.td3 import TD3CodeChecker
import random

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
letters_and_numbers = letters+numbers

days = "012"
months = "01"
months_ = "0123456789"

def random_letters(len):
    res = ''
    for i in range(round(len)):
        res = res + random.choice(letters)
    return res

def random_numbers(len):
    res = ''
    for i in range(round(len)):
        res = res + random.choice(numbers)
    return res

def radnom_date():
    day = 1 + round(random.random()*28)
    month = 1 + round(random.random()*11)
    year = round(random.random()*99)
    if day < 10:
        day = "0" + str(day)
    if month < 10:
        month = "0" + str(month)
    if year < 10:
        year = "0" + str(year)
    res = str(year) + str(month) + str(day)
    return res

def random_sex():
    sex = 'MF'
    return random.choice(sex)

def create_person():
    document_type = 'P'
    country_code = random_letters(3)
    surname = random_letters(random.random() * 10)
    given_names = random_letters(random.random() * 12)
    document_number = random_letters(random.random() * 9)
    nationality = random_letters(3)
    birth_date = radnom_date()
    sex = random_sex()
    expiry_date = radnom_date()
    code = TD3CodeGenerator(document_type, country_code, surname, given_names, document_number, nationality, birth_date, sex, expiry_date, "", {},True )
    return str(code), TD3CodeChecker(str(code),False,False).fields()

