if __name__ == "__main__" or __name__ == "queries_partition":
    from database import connect
else:
    from src.database import connect



def p_look_for_the_most_common_word(get_query: bool = False) -> str:
    # select
    QUERY = """
    WITH NounData AS (
        SELECT
            word
        FROM (
            SELECT
                regexp_split_to_table(COALESCE(string_agg(p.post_content, ' '), ''), E'\\s+') AS word
            FROM
                public.p_posts p
        ) post_words

        UNION ALL

        SELECT
            word
        FROM (
            SELECT
                regexp_split_to_table(COALESCE(string_agg(c.comment_content, ' '), ''), E'\\s+') AS word
            FROM
                public.p_comments c
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
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    conn.commit()
    conn.close()
    return QUERY


def p_raise_salary_best_moderators(get_query: bool = False):
    # update
    QUERY = """
    WITH RankedEmployees AS (
        SELECT
            e.employee_id,
            e.employee_salary,
            COUNT(p.post_id) AS post_count,
            NTILE(10) OVER (ORDER BY COUNT(p.post_id) DESC) AS percentile_rank
        FROM
            public.p_employees e
            INNER JOIN public.moderation_department m ON e.department_id = m.department_id
            LEFT JOIN public.p_posts p ON e.employee_id = p.moderator_id
        WHERE
            m.department_id IS NOT NULL
        GROUP BY
            e.employee_id, e.employee_salary
    )

    UPDATE public.p_employees
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

    conn, curr = connect(partition=True)
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def p_most_engaged_users(get_query: bool = False):
    # select
    QUERY = """
    WITH UserEngagement AS (
        SELECT
            u.user_id,
            COUNT(DISTINCT c.comment_id) AS comment_count,
            COUNT(DISTINCT p.post_id) AS post_count,
            (COUNT(DISTINCT c.comment_id) + COUNT(DISTINCT p.post_id)) AS total_engagement
        FROM
            public.p_users u
        LEFT JOIN
            public.p_comments c ON u.user_id = c.user_id
        LEFT JOIN
            public.p_posts p ON u.user_id = p.user_id
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
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    return QUERY


def p_bad_users(get_query: bool = False):
    # select
    QUERY = """
        select p_users.user_id, nb_bad_comments, nb_bad_posts, user_first_name, user_last_name from p_users 
        join (
            SELECT p_users.user_id, count(*) as nb_bad_comments from p_users
            join p_comments on p_users.user_id = p_comments.user_id
            WHERE 
            (

                (p_comments.comment_content LIKE SOME(ARRAY['%the%', '%in%', '%and%', '%own%']))
                AND
                (p_comments.user_id = p_users.user_id)
            )
            group by p_users.user_id
            order by p_users.user_id asc
        ) bad_comments on p_users.user_id = bad_comments.user_id
        join (
            SELECT p_users.user_id, count(*) as nb_bad_posts from p_users
            join p_posts on p_users.user_id = p_posts.user_id
            WHERE 
            (
                (
                    p_posts.post_content LIKE SOME(ARRAY['%fuck%', '%in%', '%and%', '%own%'])
                 or
                    p_posts.post_title LIKE SOME(ARRAY['%the%', '%in%', '%and%', '%own%'])
                )
                AND
                (p_posts.user_id = p_users.user_id)
            )
            group by p_users.user_id
            order by p_users.user_id asc
        ) bad_posts on p_users.user_id = bad_posts.user_id;
    """
    if(get_query):
        return QUERY
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    curr.fetchall()
    return QUERY


def p_get_average_age_of_users(get_query: bool = False):
    # SELECT
    conn, curr = connect(partition=True)
    QUERY = """
        select 
        avg(extract(year from age(user_date_of_birth))) as average_age, 
        min(extract(year from age(user_date_of_birth))) as min_age, 
        max(extract(year from age(user_date_of_birth))) as max_age 
        from p_users;
    """
    if(get_query):
        return QUERY

    curr.execute(QUERY)
    curr.fetchall()
    conn.close()
    return QUERY


def p_select_all_user_informations(get_query: bool = False):
    # select
    conn, curr = connect(partition=True)
    QUERY = """
    select * from p_users
        left join p_meetings on p_users.user_id = p_meetings.user_id
        left join p_posts on p_users.user_id = p_posts.user_id
        left join p_comments on p_users.user_id = p_comments.user_id
        left join sellers on p_users.user_id = sellers.user_id
        left join customers on p_users.user_id = customers.user_id;
    """
    if(get_query):
        return QUERY
    curr.execute(QUERY)
    data = curr.fetchall()
    return QUERY


def p_increase_all_employee_salaries_by_10_percent_every_year(get_query: bool = False):
    # UPDATE
    QUERY = """
    update p_employees 
    set employee_salary = employee_salary * 1.1,
    	employee_updated_at = now()
    where ((employee_updated_at < now() - interval '1 year') and (employee_salary < 5000));
    """
    if(get_query):
        return QUERY
    conn, curr = connect(partition=True)
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def p_deleting_all_user_not_connected_for_one_year(get_query: bool = False):
    # DELETE
    QUERY = """
    delete from p_users
    using p_users
        join p_meetings on p_users.user_id = p_meetings.user_id
        join p_posts on p_users.user_id = p_posts.user_id
        join p_comments on p_users.user_id = p_comments.user_id
        join sellers on p_users.user_id = sellers.user_id
        join customers on p_users.user_id = customers.user_id
    where p_users.user_id in (
        select user_id from p_users where user_last_connected < now() - interval '1 year'
    );
    """
    if(get_query):
        return QUERY
    conn, curr = connect(partition=True)
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY


def p_censorship(get_query: bool = False):
    QUERY = """
    WITH sanitized_posts AS (
    UPDATE p_posts
    SET post_content = regexp_replace(post_content, '(fuck|bitch|drug|sex)', '*******', 'gi')
    WHERE post_content ~* ANY(ARRAY['fuck', 'bitch', 'drug', 'sex'])
    RETURNING post_id, user_id, post_content
    ),
    sanitized_comments AS (
        UPDATE p_comments
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
    conn, curr = connect(partition=True)
    conn.autocommit = False
    curr.execute(QUERY)
    conn.rollback()
    conn.autocommit = True
    conn.close()
    return QUERY
