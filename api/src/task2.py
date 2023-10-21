import datetime
from lib.database import connect, insert_many


timestamp_with_timezone = (
    datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
)

users = [
    {
        "user_first_name": "Leyo",
        "user_last_name": "Lightender",
        "user_phone_number": "0658884328",
        "user_date_of_birth": "1998-08-08",
        "user_encrypted_password": "123456",
        "user_created_at": timestamp_with_timezone,
        "user_updated_at": None,
        "user_last_connected": None,
        "user_email": "leyo@email.com",
    },
    {
        "user_first_name": "leo",
        "user_last_name": "roullois",
        "user_phone_number": "0658884328",
        "user_date_of_birth": "2001-04-06",
        "user_encrypted_password": "123456",
        "user_created_at": timestamp_with_timezone,
        "user_updated_at": None,
        "user_last_connected": None,
        "user_email": "leyo@email.com",
    },
]


def get_average_age_of_users():
    # SELECT
    conn, curr = connect()
    # calculate number of years from date of birth
    QUERY = """
    SELECT AVG(EXTRACT(YEAR FROM AGE(user_date_of_birth))) FROM users;
    """
        
    curr.execute("SELECT user_date_of_birth FROM users;")
    data = curr.fetchall()
    print(data)
    conn.close()
    print("Database closed successfully")


def deleting_all_user_not_connected_for_one_year():
    # DELETE
    # Meetings, Posts, Comments, Seller, Customer, Marketplace
    QUERY = """
    DELETE FROM users
USING Users
	JOIN meetings ON Users.user_id = meetings.user_id
	JOIN posts ON Users.user_id = posts.user_id
	JOIN comments ON Users.user_id = comments.user_id
	JOIN seller ON Users.user_id = seller.user_id
	JOIN customer ON Users.user_id = customer.user_id
	JOIN marketplace ON Users.user_id = marketplace.user_id
WHERE Users.user_id IN (
    SELECT user_id FROM Users WHERE user_last_connected < NOW() - INTERVAL '1 year'
);"""
    pass


def select_all_user_sales():
    # SELECT
    pass


def select_all_user_informations(curr):
    QUERY = """
    SELECT * FROM users
        LEFT JOIN meetings ON Users.user_id = meetings.user_id
        LEFT JOIN posts ON Users.user_id = posts.user_id
        LEFT JOIN comments ON Users.user_id = comments.user_id
        LEFT JOIN seller ON Users.user_id = seller.user_id
        LEFT JOIN customer ON Users.user_id = customer.user_id;
    """
    print("QUERY :", QUERY)
    curr.execute(QUERY)
    data = curr.fetchall()
    print(data)
    return data


def increase_all_employee_salaries_by_10_percent_every_year(conn, curr):
    # UPDATE
    QUERY = """
    UPDATE employees 
    SET salary = salary * 1.1,
    	last_updated = NOW()
    WHERE last_updated < NOW() - INTERVAL '1 year';
    """
    print("QUERY :", QUERY)
    curr.execute(QUERY)
    conn.commit()


def create_new_comment(conn, curr, user_id: int, post_id: int):
    # INSERT
    comment = {
        "comment_desc": "This is a comment",
        "user_id": user_id,
        "post_id": post_id,
        "updated_at": None,
    }

    QUERY = f"""
    INSERT INTO comments ({", ".join(comment.keys())}) VALUES ({", ".join(comment.values())}
    """
    print("QUERY :", QUERY)
    curr.execute(QUERY)
    conn.commit()


def get_random_moderator_id(curr):
    # SELECT
    QUERY = """
        SELECT moderator_id FROM public."Moderation Department"
        ORDER BY RANDOM()
        LIMIT 1;
    """
    print("QUERY :", QUERY)
    curr.execute(QUERY)
    data = curr.fetchall()
    return data[0][0]


def create_a_new_post(conn, curr, user_id: int):
    # INSERT
    comment = {
        "post_title": "Title",
        "post_content": "This is a post",
        "moderator_id": get_random_moderator_id(),
        "updated_at": None,
        "user_id": user_id,
    }

    QUERY = f"""
    INSERT INTO comments ({", ".join(comment.keys())}) VALUES ({", ".join(comment.values())})
    """

    print("QUERY :", QUERY)
    curr.execute(QUERY)
    conn.commit()


def get_all_user_comments():
    # SELECT
    pass


def task2():
    conn, curr = connect()

    insert_many(conn, curr, users, "users")
    # curr.executemany(f"INSERT INTO users ({columns}) VALUES ({values});", data)
    # conn.commit()
    curr.execute("SELECT * FROM users;")
    data = curr.fetchall()
    print(data)

    conn.close()
    print("Database closed successfully")
