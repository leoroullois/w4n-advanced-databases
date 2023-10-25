import random
import time


def list_of_names():
    file = open('names.txt','r', encoding='utf8')
    names = file.read().splitlines()
    return names

def list_of_surnames():
    file = open('surnames.txt','r', encoding='utf8')
    surnames = file.read().splitlines()
    return surnames

def list_of_countries():
    file = open('countries.txt','r', encoding='utf8')
    countries = file.read().splitlines()
    return countries

def random_date(start, end, time_format, prop):

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))

def random_phone():
    phone_list = []
    for i in range(10):
        phone_list.append(random.randint(0,9))

    phone = int("".join([str(x) for x in phone_list]))
    return phone

