import datetime
from src.database import connect, insert_many
from src.utils import monitor_function


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

@monitor_function
def raise_salary_best_moderators():
    QUERY = """
WITH RankedEmployees AS (
    SELECT
        e.employee_id,
        e.employee_salary,
        COUNT(p.post_id) AS post_count,
        NTILE(10) OVER (ORDER BY COUNT(p.post_id) DESC) AS percentile_rank
    FROM
        public.employees e
        INNER JOIN public.moderation_department m ON e.department_id = m.department_id
        LEFT JOIN public.posts p ON e.employee_id = p.moderator_id
    WHERE
        m.department_id IS NOT NULL
    GROUP BY
        e.employee_id, e.employee_salary
)

UPDATE public.employees
SET employee_salary = employee_salary * 1.1
WHERE employee_id IN (
    SELECT
        employee_id
    FROM
        RankedEmployees
    WHERE
        percentile_rank = 1  -- Top 10% of employees
)
    """
    conn, curr = connect()
    curr.execute(QUERY)
    conn.commit()
    conn.close()
    print("Database closed successfully")

@monitor_function
def most_engaged_users():
    QUERY = """
WITH UserEngagement AS (
    SELECT
        u.user_id,
        COUNT(DISTINCT c.comment_id) AS comment_count,
        COUNT(DISTINCT p.post_id) AS post_count,
        (COUNT(DISTINCT c.comment_id) + COUNT(DISTINCT p.post_id)) AS total_engagement
    FROM
        public.users u
    LEFT JOIN
        public.comments c ON u.user_id = c.user_id
    LEFT JOIN
        public.posts p ON u.user_id = p.user_id
    GROUP BY
        u.user_id
)
SELECT
    user_id,
    comment_count,
    post_count,
    total_engagement,
    AVG(total_engagement) OVER () AS average_engagement
FROM
    UserEngagement
ORDER BY
    total_engagement DESC
LIMIT 100;
    """
    conn, curr = connect()
    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    print("Database closed successfully")

@monitor_function
def bad_users():
    QUERY = """
        select users.user_id, nb_bad_comments, nb_bad_posts, user_first_name, user_last_name from users 
        join (
            SELECT users.user_id, count(*) as nb_bad_comments from users
            join comments on users.user_id = comments.user_id
            WHERE 
            (

                (comments.comment_content LIKE SOME(ARRAY['%the%', '%in%', '%and%', '%own%']))
                AND
                (comments.user_id = users.user_id)
            )
            group by users.user_id
            order by users.user_id asc
        ) bad_comments on users.user_id = bad_comments.user_id
        join (
            SELECT users.user_id, count(*) as nb_bad_posts from users
            join posts on users.user_id = posts.user_id
            WHERE 
            (
                (
                    posts.post_content LIKE SOME(ARRAY['%fuck%', '%in%', '%and%', '%own%'])
                 or
                    posts.post_title LIKE SOME(ARRAY['%the%', '%in%', '%and%', '%own%'])
                )
                AND
                (posts.user_id = users.user_id)
            )
            group by users.user_id
            order by users.user_id asc
        ) bad_posts on users.user_id = bad_posts.user_id;
    """
    conn, curr = connect()
    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    print("Database closed successfully")


@monitor_function
def get_average_age_of_users():
    # SELECT
    conn, curr = connect()
    QUERY = """
        select 
        avg(extract(year from age(user_date_of_birth))) as average_age, 
        min(extract(year from age(user_date_of_birth))) as min_age, 
        max(extract(year from age(user_date_of_birth))) as max_age 
        from users;
    """
        
    curr.execute(QUERY)
    data = curr.fetchall()
    conn.close()
    print("Database closed successfully")


def deleting_all_user_not_connected_for_one_year():
    # DELETE
    QUERY = """
    delete from users
using users
	join meetings on users.user_id = meetings.user_id
	join posts on users.user_id = posts.user_id
	join comments on users.user_id = comments.user_id
	join seller on users.user_id = seller.user_id
	join customer on users.user_id = customer.user_id
	join marketplace on users.user_id = marketplace.user_id
where users.user_id in (
    select user_id from users where user_last_connected < now() - interval '1 year'
);
"""
    pass


def select_all_user_sales():
    # SELECT
    pass


@monitor_function
def select_all_user_informations(curr):
    QUERY = """
    select * from users
        left join meetings on users.user_id = meetings.user_id
        left join posts on users.user_id = posts.user_id
        left join comments on users.user_id = comments.user_id
        left join sellers on users.user_id = sellers.user_id
        left join customers on users.user_id = customers.user_id;
    """
    print("QUERY :", QUERY)
    curr.execute(QUERY)
    data = curr.fetchall()
    return data


@monitor_function
def increase_all_employee_salaries_by_10_percent_every_year(conn, curr):
    # UPDATE
    QUERY = """
    update employees 
    set employee_salary = employee_salary * 1.1,
    	employee_updated_at = now()
    where ((employee_updated_at < now() - interval '1 year') and (employee_salary < 5000));
    """
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
