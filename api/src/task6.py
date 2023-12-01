"""
Getting the cost of queries and push them to the database
"""

if __name__ == "__main__":
    from database import connect
    from task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations
else:
    from src.database import connect
    from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations

import psycopg2
import re


def get_query_cost(query: str):
    try:
        conn, curr = connect()
        explain_query = f"EXPLAIN ANALYZE {query}"
        curr.execute(explain_query)

        explain_result = curr.fetchall()
        print(explain_result)
        regex = r"cost=(\d+.\d+..\d+.\d+)"
        matches = re.findall(regex, explain_result[0][0])
        if(len(matches) == 0):
            return None
        costs = matches[0].split("..")
        if(len(costs) == 0):
            return None
        elif(len(costs) == 1):
            return float(costs[0])
        else:
            return float(costs[1])

    except psycopg2.Error as e:
        print(f"Error: {e}")

def push_cost_to_db(query_name: str, query: str, query_cost: float, index: bool = False):
    try:
        conn, curr = connect()
        query = f"INSERT INTO public.query_costs (query_name, query, query_cost, index) VALUES ('{query_name}', '', {query_cost}, {'true' if index else 'false'});"
        curr.execute(query)
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

def task6():
    index = False
    l_functions = [
            look_for_the_most_common_word,
            raise_salary_best_moderators,
            most_engaged_users,
            bad_users,
            get_average_age_of_users,
            select_all_user_informations,
            increase_all_employee_salaries_by_10_percent_every_year,
            deleting_all_user_not_connected_for_one_year
       ]

    for f in l_functions:
        query = look_for_the_most_common_word(get_query=True)
        query_name = f.__name__
        query_cost = get_query_cost(query)
        if query_cost is not None:
            print(f"{query_name} cost: {query_cost}")
            push_cost_to_db(query_name, query, query_cost, index)
        else:
            print(f"Failed to retrieve {query_name} cost.")


if __name__ == "__main__":
    task6()
