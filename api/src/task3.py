import random
import datetime
import hashlib
import json

from psycopg2.sql import NULL
from lib.database import connect, insert_many, delete_from

from src.basic_data import (
    NB_MANAGERS,
    NB_MODERATORS,
    NB_POSTS,
    NB_COMMENTS,
    NB_USERS,
    l_random_words,
    l_last_name,
    l_names,
    l_date_of_birth,
    l_phone_numbers,
    l_password,
    get_dates,
    l_countries,
    l_email,
)


def generate_users():
    users = []
    iso = lambda iso: datetime.datetime.fromisoformat(iso).astimezone().isoformat()

    for i in range(1, NB_USERS+1):
        firstname = random.choice(l_last_name)
        lastname = random.choice(l_names)
        date_of_birth = random.choice(l_date_of_birth)
        users.append(
            {
                "user_id": i,
                "user_first_name": firstname,
                "user_last_name": lastname,
                "user_phone_number": random.choice(l_phone_numbers),
                "user_date_of_birth": date_of_birth,
                "user_encrypted_password": hashlib.sha256(
                    random.choice(l_password).encode()
                ).hexdigest(),
                "user_created_at": iso(random.choice(get_dates("2021"))),
                "user_last_connected": iso(random.choice(get_dates("2023"))),
                "user_updated_at": iso(random.choice(get_dates("2022"))),
                "user_country": random.choice(l_countries),
                "user_email": f"{firstname.lower()}.{lastname.lower()}{date_of_birth[:4]}@{random.choice(l_email)}",
            }
        )

    return users


def generate_posts():
    posts = []
    iso = lambda iso: datetime.datetime.fromisoformat(iso).astimezone().isoformat()

    for i in range(1, NB_POSTS+1):
        posts.append(
            {
                "post_id": i,
                "post_title": " ".join(random.choices(l_names, k=5)),
                "post_content": " ".join(random.choices(l_names, k=10)),
                "post_created_at": iso(random.choice(get_dates("2022"))),
                "post_updated_at": iso(random.choice(get_dates("2023"))),
                "user_id": random.randint(1, NB_USERS),
                "moderator_id": random.randint(1, NB_MODERATORS),
            }
        )

    return posts


def generate_comments():
    comments = []
    iso = lambda iso: datetime.datetime.fromisoformat(iso).astimezone().isoformat()

    for i in range(1, NB_COMMENTS+1):
        comments.append(
            {
                "comment_id": i,
                "comment_content": " ".join(random.choices(l_random_words, k=10)),
                "comment_created_at": iso(random.choice(get_dates("2022"))),
                "comment_updated_at": iso(random.choice(get_dates("2023"))),
                "user_id": random.randint(1, NB_USERS),
                "post_id": random.randint(1, NB_POSTS),
            }
        )

    return comments


def generate_employees(NB_EMPLOYEES: int):
    employees = []
    iso = lambda iso: datetime.datetime.fromisoformat(iso).astimezone().isoformat()

    for i in range(1, NB_EMPLOYEES+1):
        firstname = random.choice(l_last_name)
        lastname = random.choice(l_names)
        date_of_birth = random.choice(l_date_of_birth)
        employees.append(
            {
                "employee_id": i,
                "employee_first_name": firstname,
                "employee_last_name": lastname,
                "employee_email": f"{firstname.lower()}.{lastname.lower()}{date_of_birth[:4]}@{random.choice(l_email)}",
                "employee_phone_number": random.choice(l_phone_numbers),
                "employee_date_of_birth": date_of_birth,
                "department_id": random.randint(1, 2),
                "employee_salary": random.randint(1_000, 10_000),
                "employee_created_at": iso(random.choice(get_dates("2021"))),
                "employee_updated_at": None,
            }
        )
    return employees


def generate_moderators(NB_EMPLOYEES: int):
    moderators = []
    iso = lambda iso: datetime.datetime.fromisoformat(iso).astimezone().isoformat()

    for i in range(1, NB_MODERATORS+1):
        moderators.append(
            {
                "moderator_id": i,
                "employee_id": random.randint(1, NB_EMPLOYEES),
                "department_id": 1,
                "meeting_id": None,
            }
        )
    return moderators


def generate_departments():
    departments = [
        {
            "department_id": 1,
            "department_name": "Moderation Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
        {
            "department_id": 2,
            "department_name": "Sales Moderation Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
        {
            "department_id": 3,
            "department_name": "Human Resources Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
    ]
    return departments


def delete_previous_data(conn, curr):
    delete_from(conn, curr, "comments")
    delete_from(conn, curr, "posts")
    delete_from(conn, curr, "users")
    delete_from(conn, curr, "moderation_department")
    delete_from(conn, curr, "employees")
    delete_from(conn, curr, "departments")

def task3(NB_EMPLOYEES: int):
    conn, curr = connect()

    try:
        delete_previous_data(conn, curr)

        departments = generate_departments()
        insert_many(conn, curr, departments, "departments")

        employees = generate_employees(NB_EMPLOYEES)
        insert_many(conn, curr, employees, "employees")

        moderators = generate_moderators(NB_EMPLOYEES)
        insert_many(conn, curr, moderators, "moderation_department")

        users = generate_users()
        insert_many(conn, curr, users, "users")

        posts = generate_posts()
        insert_many(conn, curr, posts, "posts")

        comments = generate_comments()
        insert_many(conn, curr, comments, "comments")
    except Exception as e:
        print("Error generating/inserting data : ", e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

