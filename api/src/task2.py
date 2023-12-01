if __name__ == "__main__" or __name__ == "task2":
    from database import connect
else:
    from src.database import connect



def look_for_the_most_common_word(get_query: bool = False) -> str:
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
    if(get_query):
        return QUERY
    conn, curr = connect()
    curr.execute(QUERY)
    conn.commit()
    conn.close()
    return QUERY


def raise_salary_best_moderators(get_query: bool = False):
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
    if(get_query):
        return QUERY

    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def most_engaged_users(get_query: bool = False):
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
    if(get_query):
        return QUERY
    conn, curr = connect()
    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    return QUERY


def bad_users(get_query: bool = False):
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
    if(get_query):
        return QUERY
    conn, curr = connect()
    curr.execute(QUERY)
    curr.fetchall()
    return QUERY


def get_average_age_of_users(get_query: bool = False):
    # SELECT
    conn, curr = connect()
    QUERY = """
        select 
        avg(extract(year from age(user_date_of_birth))) as average_age, 
        min(extract(year from age(user_date_of_birth))) as min_age, 
        max(extract(year from age(user_date_of_birth))) as max_age 
        from users;
    """
    if(get_query):
        return QUERY

    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    return QUERY


def select_all_user_informations(get_query: bool = False):
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
    if(get_query):
        return QUERY
    curr.execute(QUERY)
    data = curr.fetchall()
    return QUERY


def increase_all_employee_salaries_by_10_percent_every_year(get_query: bool = False):
    # UPDATE
    QUERY = """
    update employees 
    set employee_salary = employee_salary * 1.1,
    	employee_updated_at = now()
    where ((employee_updated_at < now() - interval '1 year') and (employee_salary < 5000));
    """
    if(get_query):
        return QUERY
    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def deleting_all_user_not_connected_for_one_year(get_query: bool = False):
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
    if(get_query):
        return QUERY
    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def censorship(get_query: bool = False):
    QUERY = """
    WITH sanitized_posts AS (
    UPDATE posts
    SET post_content = regexp_replace(post_content, '(fuck|bitch|drug|sex)', '*******', 'gi')
    WHERE post_content ~* ANY(ARRAY['fuck', 'bitch', 'drug', 'sex'])
    RETURNING post_id, user_id, post_content
    ),
    sanitized_comments AS (
        UPDATE comments
        SET comment_content = regexp_replace(comment_content, '(fuck|bitch|drug|sex)', '*******', 'gi')
        WHERE comment_content ~* ANY(ARRAY['fuck', 'bitch', 'drug', 'sex'])
        RETURNING comment_id, user_id, post_id, comment_content
    )
    SELECT
        sp.post_id,
        sp.user_id AS post_user_id,
        sp.post_content AS sanitized_post_content,
        sc.comment_id,
        sc.user_id AS comment_user_id,
        sc.post_id AS comment_post_id,
        sc.comment_content AS sanitized_comment_content
    FROM sanitized_posts sp
    JOIN sanitized_comments sc ON sp.post_id = sc.post_id;
    """
    if(get_query):
        return QUERY
    conn, curr = connect()
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY
