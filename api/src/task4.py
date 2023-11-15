from src.database import connect

from src.task3 import task3
from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations


def clean_logs():
    conn, curr = connect()
    try:
        curr.execute("DELETE FROM logs;")
        conn.commit()
    except Exception as e:
        print("[ERROR] Cleaning: ", e)
    finally:
        conn.close()

def fetch_logs():
    conn, curr = connect()
    try:
        curr.execute("SELECT * FROM logs;")
        return curr.fetchall()
    except Exception as e:
        print("[ERROR] Fetching: ", e)
    finally:
        conn.close()

def task4():
    logs = None
    clean_logs()

    for _ in range(2):
        # select_all_user_informations()
        # bad_users()
        # deleting_all_user_not_connected_for_one_year()
        # increase_all_employee_salaries_by_10_percent_every_year()
        # get_average_age_of_users()
        # most_engaged_users()
        raise_salary_best_moderators()
        # look_for_the_most_common_word()
        

    logs = fetch_logs()
    return logs
