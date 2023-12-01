"""
Task 5, 6 and 7
Create indexes, launch a benchmark with and without indexes and push the result in the database.
"""

if __name__ == "__main__":
    from database import connect
    from utils import monitor_function
    from task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship
else:
    from src.database import connect
    from src.utils import monitor_function
    from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship


def delete_all_indexes():
    QUERY = """
    drop index if exists idx_users;
    drop index if exists idx_posts;
    drop index if exists idx_comments;
    drop index if exists idx_sales_of_user;
    drop index if exists idx_employees;
    drop index if exists idx_salary_updated_at;
    drop index if exists idx_post_user;
    drop index if exists idx_comment_user;
    """
    conn, curr = connect()
    curr.execute(QUERY)
    conn.commit()
    conn.close()

def create_index(name: str, table: str, column: str, type: str):
    QUERY = f"""
    CREATE INDEX IF NOT EXISTS {name}
    ON {table} USING {type} ({column});
    """
    print(QUERY)
    conn, curr = connect()
    curr.execute(QUERY)
    conn.commit()
    conn.close()


def create_indexes_btree():
    # Will be used as the primary indexes

    create_index("idx_users", "users", "user_created_at", "btree")
    create_index("idx_sales_of_user", "marketplace", "seller_id", "btree")
    # create_index("idx_posts", "posts", "post_content", "btree")
    # create_index("idx_comments", "comments", "comment_content", "btree")
    # create_index("idx_employees", "employees", "employee_salary", "btree")
    print("-------------- INDEXES CREATED BTREE -----------------")


def create_indexes_hash():
    # Will be used for experimental purposes
    create_index("idx_users", "users", "user_created_at", "hash")
    create_index("idx_sales_of_user", "marketplace", "seller_id", "hash")
    # create_index("idx_posts", "posts", "post_content", "hash")
    # create_index("idx_comments", "comments", "comment_content", "hash")
    # create_index("idx_employees", "employees", "employee_salary", "hash")
    print("-------------- INDEXES CREATED HASH -----------------")


def create_function_index():
    IDX_POST_CONTENT = """
    CREATE INDEX IF NOT EXISTS idx_post_content
    ON posts USING gin(to_tsvector('english', post_content));
    """

    IDX_COMMENT_CONTENT = """
    CREATE INDEX IF NOT EXISTS idx_comment_content
    ON comments USING gin(to_tsvector('english', comment_content));
    """
    conn, curr = connect()
    curr.execute(IDX_COMMENT_CONTENT)
    curr.execute(IDX_POST_CONTENT)
    conn.commit()
    conn.close()


def create_indexes_composite():
    IDX_COMPOSITE_EMPLOYEE = """
    CREATE INDEX idx_salary_updated_at ON employees (employee_salary, employee_updated_at);
    """

    IDX_COMPOSITE_POST = """
    CREATE INDEX idx_post_user ON posts (post_id, user_id);
    """

    IDX_COMPOSITE_COMMENT = """
    CREATE INDEX idx_comment_user ON comments (comment_id, user_id);
    """

    conn, curr = connect()
    curr.execute(IDX_COMPOSITE_EMPLOYEE)
    curr.execute(IDX_COMPOSITE_POST)
    curr.execute(IDX_COMPOSITE_COMMENT)
    conn.commit()
    conn.close()   

def run_index_tests(index_name: str, NB_ITERATIONS: int = 1):
    for _ in range(NB_ITERATIONS):
        monitor_function(select_all_user_informations, index=True, index_name=index_name)()
        monitor_function(raise_salary_best_moderators, index=True, index_name=index_name)()
        monitor_function(look_for_the_most_common_word, index=True, index_name=index_name)()
        monitor_function(most_engaged_users, index=True, index_name=index_name)()
        monitor_function(get_average_age_of_users, index=True, index_name=index_name)()
        monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=True, index_name=index_name)()
        monitor_function(censorship, index=True, index_name=index_name)()
        monitor_function(bad_users, index=True, index_name=index_name)()
        # monitor_function(deleting_all_user_not_connected_for_one_year, index=True, index_name=index_name)()


def task5():
    NB_ITERATIONS = 1
    index_names = ["hash", "btree", "btree+composite", "btree+function", "btree+composite+function"]
    delete_all_indexes()
    
    for _ in range(NB_ITERATIONS):
            monitor_function(select_all_user_informations, index=False)()
            monitor_function(raise_salary_best_moderators, index=False)()
            monitor_function(look_for_the_most_common_word, index=False)()
            monitor_function(most_engaged_users, index=False)()
            monitor_function(get_average_age_of_users, index=False)()
            monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=False)()
            monitor_function(bad_users, index=False)()
            monitor_function(censorship, index=False)()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()

    for index_name in index_names:
        delete_all_indexes()
        
        if index_name == "hash":
            create_indexes_hash()
            run_index_tests(index_name, NB_ITERATIONS)
        elif index_name == "btree":
            delete_all_indexes()
            create_indexes_btree()
            run_index_tests(index_name, NB_ITERATIONS)
        elif index_name == "btree+composite":
            delete_all_indexes()
            create_indexes_btree()
            create_indexes_composite()
            run_index_tests(index_name, NB_ITERATIONS)
        elif index_name == "btree+function":
            delete_all_indexes()
            create_indexes_btree()
            create_function_index()
            run_index_tests(index_name, NB_ITERATIONS)
        elif index_name == "btree+composite+function":
            delete_all_indexes()
            create_indexes_btree()
            create_indexes_composite()
            create_function_index()
            run_index_tests(index_name, NB_ITERATIONS)


if __name__ == "__main__":
    task5()
