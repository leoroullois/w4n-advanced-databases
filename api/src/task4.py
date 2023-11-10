from src.database import connect

from src.task3 import task3
from src.task2 import bad_users, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, most_engaged_users, raise_salary_best_moderators, select_all_user_informations


def clean_logs(conn, curr):
    try:
        curr.execute("DELETE FROM logs;")
        conn.commit()
    except Exception as e:
        print("[ERROR] Cleaning: ", e)
    finally:
        conn.close()

def fetch_logs(conn, curr):
    try:
        curr.execute("SELECT * FROM logs;")
        return curr.fetchall()
    except Exception as e:
        print("[ERROR] Fetching: ", e)
    finally:
        conn.close()

def task4(
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
    conn, curr = connect()

    logs = None
    # clean_logs(conn, curr)

    for _ in range(20):
        increase_all_employee_salaries_by_10_percent_every_year(conn, curr)
        # select_all_user_informations(curr)
        get_average_age_of_users()
        bad_users()
        most_engaged_users()
        raise_salary_best_moderators()
        

    # task3(
    #     NB_EMPLOYEES=NB_EMPLOYEES,
    #     NB_MANAGERS=NB_MANAGERS,
    #     NB_MODERATORS=NB_MODERATORS,
    #     NB_USERS=NB_USERS,
    #     NB_POSTS=NB_POSTS,
    #     NB_COMMENTS=NB_COMMENTS,
    #     NB_CUSTOMERS=NB_CUSTOMERS,
    #     NB_SELLERS=NB_SELLERS,
    #     NB_HUMAN_RESOURCES=NB_HUMAN_RESOURCES,
    #     NB_SALES_MODERATORS=NB_SALES_MODERATORS,
    #         )
    logs = fetch_logs(conn, curr)
    return logs
