if __name__ == "__main__":
    from database import connect
    from utils import monitor_function
    from task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations
else:
    from src.database import connect
    from src.utils import monitor_function
    from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations


def delete_all_indexes():
    QUERY = """
    drop index if exists idx_users;
    drop index if exists idx_posts;
    drop index if exists idx_comments;
    drop index if exists idx_sales_of_user;
    drop index if exists idx_employees;
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

    create_index("idx_users", "users", "user_created_at", "btree")
    create_index("idx_posts", "posts", "post_content", "btree")
    create_index("idx_comments", "comments", "comment_content", "btree")
    create_index("idx_sales_of_user", "marketplace", "seller_id", "btree")
    create_index("idx_employees", "employees", "employee_salary", "btree")
    print("-------------- INDEXES CREATED BTREE -----------------")


def create_indexes_hash():

    create_index("idx_users", "users", "user_created_at", "hash")
    create_index("idx_posts", "posts", "post_content", "hash")
    create_index("idx_comments", "comments", "comment_content", "hash")
    create_index("idx_sales_of_user", "marketplace", "seller_id", "hash")
    create_index("idx_employees", "employees", "employee_salary", "hash")
    print("-------------- INDEXES CREATED HASH -----------------")


def create_indexes_function():
    IDX_POSTS = """
    CREATE INDEX idx_posts ON posts 
    USING btree 
    (
        regexp_split_to_table(COALESCE(string_agg(p.post_content, ' '), ''), E'\\s+')
    );
    """
    IDX_COMMENTS = """
    CREATE INDEX IF NOT EXISTS idx_comments 
    ON comments USING gist (comment_id);
    """

    conn, curr = connect()
    curr.execute(IDX_POSTS)
    curr.execute(IDX_COMMENTS)
    conn.commit()
    conn.close()
    


def task5():
    logs = None
    # clean_logs()

    # ? no bitmap indexes in postgresql ?
    index_names = ["btree", "hash"]

    delete_all_indexes()
    
    # for _ in range(1):
    #         monitor_function(select_all_user_informations, index=False)()
    #         monitor_function(raise_salary_best_moderators, index=False)()
    #         monitor_function(look_for_the_most_common_word, index=False)()
    #         monitor_function(most_engaged_users, index=False)()
    #         monitor_function(get_average_age_of_users, index=False)()
    #         monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=False)()
    #         # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()
    #         monitor_function(bad_users, index=False)()

    for index_name in index_names:
        delete_all_indexes()
        
        if index_name == "btree":
            create_indexes_btree()
        elif index_name == "hash":
            create_indexes_hash()
        for _ in range(1):
            monitor_function(select_all_user_informations, index=True, index_name=index_name)()
            monitor_function(raise_salary_best_moderators, index=True, index_name=index_name)()
            monitor_function(look_for_the_most_common_word, index=True, index_name=index_name)()
            monitor_function(most_engaged_users, index=True, index_name=index_name)()
            monitor_function(get_average_age_of_users, index=True, index_name=index_name)()
            monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=True, index_name=index_name)()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=True, index_name=index_name)()
            monitor_function(bad_users, index=True, index_name=index_name)()

if __name__ == "__main__":
    task5()
