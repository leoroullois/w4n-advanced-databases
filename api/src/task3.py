import random
import hashlib

from essential_generators import DocumentGenerator

from src.database import connect, insert_many, delete_from

from src.data_generator import (
    list_of_names,
    list_of_surnames,
    list_of_countries,
    list_of_passwords,
    random_date,
    random_phone,
)

from src.utils import monitor_function

GENERATOR = DocumentGenerator()

MODERATION_DEPARTMENT_ID = 1
SALES_MODERATION_DEPARTMENT_ID = 2
HUMAN_RESOURCES_DEPARTMENT_ID = 3

l_email = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "mail.com",
    "aol.com",
    "yandex.com",
    "zoho.com",
    "protonmail.com",
    "gmx.com",
    "tutanota.com",
    "mail.ru",
    "yopmail.com",
    "gmx.de",
    "gmx.at",
    "gmx.ch",
    "gmx.net",
    "gmx.fr",
    "gmx.us",
]


@monitor_function
def generate_users(NB_USERS: int):
    users = []

    for i in range(1, NB_USERS + 1):
        # Defining basing user info
        firstname = random.choice(list_of_names())
        lastname = random.choice(list_of_surnames())
        date_of_birth = random_date("1970-1-1", "2010-1-1", "%Y-%m-%d", random.random())

        # Adding all of the user info into a single table
        users.append(
            {
                "user_id": i,
                "user_first_name": firstname,
                "user_last_name": lastname,
                "user_phone_number": str(random_phone()),
                "user_date_of_birth": date_of_birth,
                "user_encrypted_password": hashlib.sha256(
                    random.choice(list_of_passwords()).encode()
                ).hexdigest(),
                "user_created_at": random_date(
                    "2000-1-1 1:30 PM",
                    "2016-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "user_last_connected": random_date(
                    "2016-1-1 1:30 PM",
                    "2023-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "user_updated_at": random_date(
                    "2016-1-1 1:30 PM",
                    "2023-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "user_country": random.choice(list_of_countries()),
                "user_email": f"{firstname.lower()}.{lastname.lower()}{date_of_birth[:4]}@{random.choice(l_email)}",
            }
        )

    return users


@monitor_function
def generate_posts(NB_POSTS: int, NB_USERS: int, NB_MODERATORS: int):
    posts = []

    for i in range(1, NB_POSTS + 1):
        posts.append(
            {
                "post_id": i,
                "post_title": f"{GENERATOR.sentence()}",
                "post_content": f"{GENERATOR.paragraph()}",
                "post_created_at": random_date(
                    "2000-1-1 1:30 PM",
                    "2016-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "post_updated_at": random_date(
                    "2000-1-1 1:30 PM",
                    "2016-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "user_id": random.randint(1, NB_USERS),
                "moderator_id": random.randint(1, NB_MODERATORS),
            }
        )

    return posts


@monitor_function
def generate_comments(NB_COMMENTS: int, NB_USERS: int, NB_POSTS: int):
    comments = []

    for i in range(1, NB_COMMENTS + 1):
        comments.append(
            {
                "comment_id": i,
                "comment_content": f"{GENERATOR.sentence()}",
                "comment_created_at": random_date(
                    "2000-1-1 1:30 PM",
                    "2016-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "comment_updated_at": random_date(
                    "2000-1-1 1:30 PM",
                    "2016-1-1 4:50 AM",
                    "%Y-%m-%d %I:%M %p",
                    random.random(),
                ),
                "user_id": random.randint(1, NB_USERS),
                "post_id": random.randint(1, NB_POSTS),
            }
        )

    return comments


@monitor_function
def generate_employees(NB_EMPLOYEES: int):
    employees = []

    for i in range(1, NB_EMPLOYEES + 1):
        firstname = random.choice(list_of_names())
        lastname = random.choice(list_of_surnames())
        date_of_birth = random_date("1970-1-1", "2010-1-1", "%Y-%m-%d", random.random())
        employees.append(
            {
                "employee_id": i,
                "employee_first_name": firstname,
                "employee_last_name": lastname,
                "employee_email": f"{firstname.lower()}.{lastname.lower()}{date_of_birth[:4]}@{random.choice(l_email)}",
                "employee_phone_number": str(random_phone()),
                "employee_date_of_birth": date_of_birth,
                "department_id": random.randint(1, 2),
                "employee_salary": random.randint(1_000, 10_000),
                "employee_created_at": random_date(
                    "1970-1-1", "2010-1-1", "%Y-%m-%d", random.random()
                ),
                "employee_updated_at": None,
            }
        )
    return employees


@monitor_function
def generate_moderators(NB_EMPLOYEES: int, NB_MODERATORS: int):
    moderators = []
    for i in range(1, NB_MODERATORS + 1):
        moderators.append(
            {
                "moderator_id": i,
                "employee_id": random.randint(1, NB_EMPLOYEES),
                "department_id": 1,
                "meeting_id": None,
            }
        )
    return moderators


@monitor_function
def generate_departments(NB_MANAGERS: int):
    departments = [
        {
            "department_id": MODERATION_DEPARTMENT_ID,
            "department_name": "Moderation Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
        {
            "department_id": SALES_MODERATION_DEPARTMENT_ID,
            "department_name": "Sales Moderation Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
        {
            "department_id": HUMAN_RESOURCES_DEPARTMENT_ID,
            "department_name": "Human Resources Department",
            "manager_id": random.randint(1, NB_MANAGERS),
        },
    ]
    return departments


@monitor_function
def generate_marketplace(NB_CUSTOMERS: int, NB_SELLERS: int, NB_SALES_MODERATORS: int):
    # sale_id, sale_title, sale_desc, sale_price, customer_id, seller_id, sales_rep_id
    marketplace = []
    for i in range(1, NB_CUSTOMERS + 1):
        marketplace.append(
            {
                "sale_id": i,
                "sale_title": f"{GENERATOR.sentence()}",
                "sale_desc": f"{GENERATOR.paragraph(3)}",
                "sale_price": random.randint(1, 1000),
                "customer_id": i,
                "seller_id": random.randint(1, NB_SELLERS),
                "sales_rep_id": random.randint(1, NB_SALES_MODERATORS),
            }
        )
    return marketplace


@monitor_function
def generate_sales_moderation_department(
    NB_SALES_MODERATORS: int, NB_MANAGERS: int, NB_SELLERS: int
):
    # sales_rep_id, sale_id, manager_id, department_id, employee_id
    sales_moderation_department = []
    for i in random.sample(
        [i for i in range(1, NB_SALES_MODERATORS + 1)], NB_SALES_MODERATORS
    ):
        sales_moderation_department.append(
            {
                "sales_rep_id": i,
                "sale_id": random.randint(1, NB_SELLERS),
                "manager_id": random.randint(1, NB_MANAGERS),
                "department_id": SALES_MODERATION_DEPARTMENT_ID,
                "employee_id": i,
            }
        )
    return sales_moderation_department


@monitor_function
def generate_human_resources_department(NB_HUMAN_RESOURCES: int, NB_EMPLOYEES: int):
    # resources_id, employee_id, department_id
    human_resources_department = []
    for i in range(1, NB_HUMAN_RESOURCES + 1):
        human_resources_department.append(
            {
                "resources_id": i,
                "employee_id": random.randint(1, NB_EMPLOYEES),
                "department_id": HUMAN_RESOURCES_DEPARTMENT_ID,
            }
        )
    return human_resources_department


@monitor_function
def delete_previous_data(conn, curr):
    delete_from(conn, curr, "comments")
    delete_from(conn, curr, "posts")
    delete_from(conn, curr, "marketplace")
    delete_from(conn, curr, "moderation_department")
    delete_from(conn, curr, "sales_moderation_department")
    delete_from(conn, curr, "human_resources_department")
    delete_from(conn, curr, "employees")
    delete_from(conn, curr, "departments")
    delete_from(conn, curr, "sellers")
    delete_from(conn, curr, "customers")
    delete_from(conn, curr, "meetings")
    delete_from(conn, curr, "users")


@monitor_function
def push_departments(conn,curr, NB_MANAGERS):
    departments = generate_departments(NB_MANAGERS)
    insert_many(conn, curr, departments, "departments")


@monitor_function
def push_employees(conn, curr, NB_EMPLOYEES):
    employees = generate_employees(NB_EMPLOYEES)
    insert_many(conn, curr, employees, "employees")

@monitor_function
def push_moderators(conn, curr, NB_EMPLOYEES, NB_MODERATORS):
    moderators = generate_moderators(NB_EMPLOYEES, NB_MODERATORS)
    insert_many(conn, curr, moderators, "moderation_department")

@monitor_function
def push_sales_moderation_department(conn, curr, NB_MODERATORS, NB_MANAGERS, NB_SELLERS):
    sales_moderation_department = generate_sales_moderation_department(
        NB_MODERATORS, NB_MANAGERS, NB_SELLERS
    )
    insert_many(conn, curr, sales_moderation_department, "sales_moderation_department")

@monitor_function
def push_human_resources_department(conn, curr, NB_HUMAN_RESOURCES, NB_EMPLOYEES):
    human_resources_department = generate_human_resources_department(
        NB_HUMAN_RESOURCES, NB_EMPLOYEES
    )
    insert_many(conn, curr, human_resources_department, "human_resources_department")

@monitor_function
def push_users(conn, curr, NB_USERS):
    users = generate_users(NB_USERS)
    insert_many(conn, curr, users, "users")
    return users

@monitor_function
def push_posts(conn, curr, NB_POSTS, NB_USERS, NB_MODERATORS):
    posts = generate_posts(NB_POSTS, NB_USERS, NB_MODERATORS)
    insert_many(conn, curr, posts, "posts")

@monitor_function
def push_comments(conn, curr, NB_COMMENTS, NB_USERS, NB_POSTS):
    comments = generate_comments(NB_COMMENTS, NB_USERS, NB_POSTS)
    insert_many(conn, curr, comments, "comments")


@monitor_function
def push_customers(conn, curr,users, NB_CUSTOMERS):
    customers = [
        {"customer_id": i + 1, "user_id": elt["user_id"]}
        for i, elt in enumerate(random.sample(users, NB_CUSTOMERS))
    ]
    insert_many(conn, curr, customers, "customers")

@monitor_function
def push_sellers(conn, curr, users, NB_SELLERS):
    sellers = [
        {"seller_id": i + 1, "user_id": elt["user_id"]}
        for i, elt in enumerate(random.sample(users, NB_SELLERS))
    ]
    insert_many(conn, curr, sellers, "sellers")

@monitor_function
def push_marketplace(conn, curr, NB_CUSTOMERS, NB_SELLERS, NB_SALES_MODERATORS):
    marketplace = generate_marketplace(NB_CUSTOMERS, NB_SELLERS, NB_SALES_MODERATORS)
    insert_many(conn, curr, marketplace, "marketplace")

def task3(
    NB_EMPLOYEES: int = 10,
    NB_MANAGERS: int = 10,
    NB_MODERATORS: int = 10,
    NB_USERS: int = 100,
    NB_POSTS: int = 100,
    NB_COMMENTS: int = 100,
    NB_CUSTOMERS: int = 50,
    NB_SELLERS: int = 10,
    NB_HUMAN_RESOURCES: int = 6,
    NB_SALES_MODERATORS: int = 6,
):
    """
    Generate data for task 3

    NB_MANAGERS needs to be lower than NB_EMPLOYEES
    NB_MODERATORS needs to be lower than NB_EMPLOYEES
    NB_SALES_MODERATORS needs to be lower than NB_EMPLOYEES
    NB_HUMAN_RESOURCES needs to be lower than NB_EMPLOYEES

    NB_CUSTOMERS needs to be lower than NB_USERS
    NB_SELLERS needs to be lower than NB_USERS
    """
    conn, curr = connect()

    delete_previous_data(conn, curr)

    push_departments(conn,curr, NB_MANAGERS)
    push_employees(conn, curr, NB_EMPLOYEES)
    push_moderators(conn,curr, NB_EMPLOYEES, NB_MODERATORS)
    push_sales_moderation_department(conn,curr, NB_MODERATORS, NB_MANAGERS, NB_SELLERS)
    push_human_resources_department(conn,curr, NB_HUMAN_RESOURCES, NB_EMPLOYEES)
    users = push_users(conn,curr, NB_USERS)
    push_posts(conn,curr, NB_POSTS, NB_USERS, NB_MODERATORS)
    push_comments(conn,curr, NB_COMMENTS, NB_USERS, NB_POSTS)
    push_customers(conn,curr, users, NB_CUSTOMERS)
    push_sellers(conn,curr, users, NB_SELLERS)
    push_marketplace(conn,curr, NB_CUSTOMERS, NB_SELLERS, NB_SALES_MODERATORS)

    conn.commit()
    conn.close()
