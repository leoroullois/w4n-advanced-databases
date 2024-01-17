if __name__ == "__main__":
    from database import connect
    from utils import monitor_function
    from task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship
    from columnar_queries import c_bad_users, c_censorship, c_deleting_all_user_not_connected_for_one_year, c_get_average_age_of_users, c_increase_all_employee_salaries_by_10_percent_every_year, c_look_for_the_most_common_word, c_most_engaged_users, c_raise_salary_best_moderators, c_select_all_user_informations
else:
    from src.database import connect
    from src.utils import monitor_function
    from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship
    from src.columnar_queries import c_bad_users, c_censorship, c_deleting_all_user_not_connected_for_one_year, c_get_average_age_of_users, c_increase_all_employee_salaries_by_10_percent_every_year, c_look_for_the_most_common_word, c_most_engaged_users, c_raise_salary_best_moderators, c_select_all_user_informations


def create_columnar_employees_table():
    """
    Create a columnar table for employees using citus postgresql extension
    """

    QUERY = """
        DO
        $do$
        BEGIN
            IF NOT EXISTS (
              SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'c_employees'
            ) THEN
                CREATE TABLE IF NOT EXISTS c_employees(LIKE employees) USING COLUMNAR;
                insert into c_employees (select * from employees);
            END IF;
        END
        $do$
    """
    
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    conn.commit()
    

def create_columnar_users_table():
    QUERY = """
        DO
        $do$
        BEGIN
            IF NOT EXISTS (
              SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'c_users'
            ) THEN
                CREATE TABLE IF NOT EXISTS c_users(LIKE users) USING COLUMNAR;
                insert into c_users (select * from users);
            END IF;
        END
        $do$
    """
    
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    conn.commit()


def create_columnar_posts_table():
    QUERY = """
        DO
        $do$
        BEGIN
            IF NOT EXISTS (
              SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'c_posts'
            ) THEN
                CREATE TABLE IF NOT EXISTS c_posts(LIKE posts) USING COLUMNAR;
                insert into c_posts (select * from posts);
            END IF;
        END
        $do$
    """
    
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    conn.commit()


def create_columnar_comments_table():
    QUERY = """
        DO
        $do$
        BEGIN
            IF NOT EXISTS (
              SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'c_comments'
            ) THEN
                CREATE TABLE IF NOT EXISTS c_comments(LIKE comments) USING COLUMNAR;
                insert into c_comments (select * from comments);
            END IF;
        END
        $do$
    """
    
    conn, curr = connect(partition=True)
    curr.execute(QUERY)
    conn.commit()

def benchmark():
    NB_ITERATIONS = 9
    
    for _ in range(NB_ITERATIONS):
            monitor_function(select_all_user_informations, index=False)()
            # monitor_function(raise_salary_best_moderators, index=False)()
            monitor_function(look_for_the_most_common_word, index=False)()
            monitor_function(most_engaged_users, index=False)()
            monitor_function(get_average_age_of_users, index=False)()
            # monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=False)()
            monitor_function(bad_users, index=False)()
            # monitor_function(censorship, index=False)()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()


    for _ in range(NB_ITERATIONS):
            monitor_function(c_select_all_user_informations, partition=True, partition_db=True)()
            # monitor_function(c_raise_salary_best_moderators, partition=True, partition_db=True)()
            monitor_function(c_look_for_the_most_common_word, partition=True, partition_db=True)()
            monitor_function(c_most_engaged_users, partition=True, partition_db=True)()
            monitor_function(c_get_average_age_of_users, partition=True, partition_db=True)()
            # monitor_function(c_increase_all_employee_salaries_by_10_percent_every_year, partition=True, partition_db=True)()
            monitor_function(c_bad_users, partition=True, partition_db=True)()
            # monitor_function(c_censorship, partition=True, partition_db=True)()
            # monitor_function(c_deleting_all_user_not_connected_for_one_year, partition=True)()


def main():
    create_columnar_employees_table()
    create_columnar_users_table()
    create_columnar_posts_table()
    create_columnar_comments_table()
    benchmark()

if __name__ == "__main__":
    main()
