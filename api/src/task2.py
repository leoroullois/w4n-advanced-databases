from src.database import connect


def look_for_the_most_common_word():
    # select
    QUERY = """
    WITH NounData AS (
        SELECT
            word
        FROM (
            SELECT
                regexp_split_to_table(COALESCE(string_agg(p.post_content, ' '), ''), E'\\s+') AS word
            FROM
                public.posts p
        ) post_words

        UNION ALL

        SELECT
            word
        FROM (
            SELECT
                regexp_split_to_table(COALESCE(string_agg(c.comment_content, ' '), ''), E'\\s+') AS word
            FROM
                public.comments c
        ) comment_words
    )

    SELECT
        word,
        COUNT(*) AS frequency
    FROM
        NounData
    WHERE
        LENGTH(word) > 5
    GROUP BY
        word
    ORDER BY
        frequency DESC
    LIMIT 20;
    """
    conn, curr = connect()
    curr.execute(QUERY)
    conn.commit()
    conn.close()


def raise_salary_best_moderators():
    # update
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
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()


def most_engaged_users():
    # select
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


def bad_users():
    # select
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
    curr.fetchall()
    conn.close()


def select_all_user_informations():
    # select
    conn, curr = connect()
    QUERY = """
    select * from users
        left join meetings on users.user_id = meetings.user_id
        left join posts on users.user_id = posts.user_id
        left join comments on users.user_id = comments.user_id
        left join sellers on users.user_id = sellers.user_id
        left join customers on users.user_id = customers.user_id;
    """
    curr.execute(QUERY)
    data = curr.fetchall()
    return data


def increase_all_employee_salaries_by_10_percent_every_year():
    # UPDATE
    QUERY = """
    update employees 
    set employee_salary = employee_salary * 1.1,
    	employee_updated_at = now()
    where ((employee_updated_at < now() - interval '1 year') and (employee_salary < 5000));
    """
    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()


def deleting_all_user_not_connected_for_one_year():
    # DELETE
    QUERY = """
    delete from users
    using users
        join meetings on users.user_id = meetings.user_id
        join posts on users.user_id = posts.user_id
        join comments on users.user_id = comments.user_id
        join sellers on users.user_id = sellers.user_id
        join customers on users.user_id = customers.user_id
    where users.user_id in (
        select user_id from users where user_last_connected < now() - interval '1 year'
    );
"""
    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()


def task2():
    conn, curr = connect()

    conn.close()
