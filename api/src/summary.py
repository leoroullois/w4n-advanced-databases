if __name__ == "__main__":
    from database import connect
    from utils import monitor_function
    from task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship
    from columnar_queries import c_bad_users, c_censorship, c_deleting_all_user_not_connected_for_one_year, c_get_average_age_of_users, c_increase_all_employee_salaries_by_10_percent_every_year, c_look_for_the_most_common_word, c_most_engaged_users, c_raise_salary_best_moderators, c_select_all_user_informations
    from queries_partition import p_bad_users, p_censorship, p_deleting_all_user_not_connected_for_one_year, p_get_average_age_of_users, p_increase_all_employee_salaries_by_10_percent_every_year, p_look_for_the_most_common_word, p_most_engaged_users, p_raise_salary_best_moderators, p_select_all_user_informations
else:
    from src.database import connect
    from src.utils import monitor_function
    from src.task2 import bad_users, deleting_all_user_not_connected_for_one_year, get_average_age_of_users, increase_all_employee_salaries_by_10_percent_every_year, look_for_the_most_common_word, most_engaged_users, raise_salary_best_moderators, select_all_user_informations, censorship
    from src.queries_partition import p_bad_users, p_censorship, p_deleting_all_user_not_connected_for_one_year, p_get_average_age_of_users, p_increase_all_employee_salaries_by_10_percent_every_year, p_look_for_the_most_common_word, p_most_engaged_users, p_raise_salary_best_moderators, p_select_all_user_informations
    from src.columnar_queries import c_bad_users, c_censorship, c_deleting_all_user_not_connected_for_one_year, c_get_average_age_of_users, c_increase_all_employee_salaries_by_10_percent_every_year, c_look_for_the_most_common_word, c_most_engaged_users, c_raise_salary_best_moderators, c_select_all_user_informations

def method0():
    NB_ITERATIONS = 10

    for _ in range(NB_ITERATIONS):

            # ORIGINAL
            monitor_function(select_all_user_informations, index=False)()
            monitor_function(raise_salary_best_moderators, index=False)()
            monitor_function(look_for_the_most_common_word, index=False)()
            monitor_function(most_engaged_users, index=False)()
            monitor_function(get_average_age_of_users, index=False)()
            monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=False)()
            monitor_function(bad_users, index=False)() # indexing
            monitor_function(censorship, index=False)()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()

def method1():
    NB_ITERATIONS = 9

    for _ in range(NB_ITERATIONS):

            # ORIGINAL
            # monitor_function(select_all_user_informations, index=False)()
            # monitor_function(raise_salary_best_moderators, index=False)()
            # monitor_function(look_for_the_most_common_word, index=False)()
            # monitor_function(most_engaged_users, index=False)()
            # monitor_function(get_average_age_of_users, index=False)()
            # monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=False)()
            monitor_function(bad_users, index=True)() # indexing
            # monitor_function(censorship, index=False)()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()

            # PARTITION
            monitor_function(p_select_all_user_informations, partition=True, partition_db=True)()
            monitor_function(p_raise_salary_best_moderators, partition=True, partition_db=True)()
            # monitor_function(p_look_for_the_most_common_word, partition=True, partition_db=True)()
            # monitor_function(p_most_engaged_users, partition=True, partition_db=True)()
            monitor_function(p_get_average_age_of_users, partition=True, partition_db=True)()
            monitor_function(p_increase_all_employee_salaries_by_10_percent_every_year, partition=True, partition_db=True)()
            # monitor_function(p_bad_users, partition=True, partition_db=True)()
            monitor_function(p_censorship, partition=True, partition_db=True)()
            # monitor_function(p_deleting_all_user_not_connected_for_one_year, partition=True)()

            # COLUMNAR
            # monitor_function(c_select_all_user_informations, partition=True, partition_db=True)()
            # monitor_function(c_raise_salary_best_moderators, partition=True, partition_db=True)()
            monitor_function(c_look_for_the_most_common_word, partition=True, partition_db=True)()
            monitor_function(c_most_engaged_users, partition=True, partition_db=True)()
            # monitor_function(c_get_average_age_of_users, partition=True, partition_db=True)()
            # monitor_function(c_increase_all_employee_salaries_by_10_percent_every_year, partition=True, partition_db=True)()
            # monitor_function(c_bad_users, partition=True, partition_db=True)()
            # monitor_function(c_censorship, partition=True, partition_db=True)()
            # monitor_function(c_deleting_all_user_not_connected_for_one_year, partition=True)()
    pass

def method2():
    NB_ITERATIONS = 5

    for _ in range(NB_ITERATIONS):
            # ORIGINAL
            # monitor_function(select_all_user_informations, index=False)()
            monitor_function(raise_salary_best_moderators, index=True, method="method2")() # indexing
            # monitor_function(look_for_the_most_common_word, index=False)()
            monitor_function(most_engaged_users, index=True, method="method2")() # indexing
            monitor_function(get_average_age_of_users, index=False, method="method2")()
            monitor_function(increase_all_employee_salaries_by_10_percent_every_year, index=True, method="method2")()
            # monitor_function(bad_users, index=False)()
            monitor_function(censorship, index=False, method="method2")()
            # monitor_function(deleting_all_user_not_connected_for_one_year, index=False)()

            # PARTITION
            # monitor_function(p_select_all_user_informations, partition=True, partition_db=True)()
            # monitor_function(p_raise_salary_best_moderators, partition=True, partition_db=True)()
            monitor_function(p_look_for_the_most_common_word, partition=True, partition_db=True, method="method2")()
            # monitor_function(p_most_engaged_users, partition=True, partition_db=True)()
            # monitor_function(p_get_average_age_of_users, partition=True, partition_db=True)()
            # monitor_function(p_increase_all_employee_salaries_by_10_percent_every_year, partition=True, partition_db=True)()
            # monitor_function(p_bad_users, partition=True, partition_db=True)()
            # monitor_function(p_censorship, partition=True, partition_db=True)()
            # monitor_function(p_deleting_all_user_not_connected_for_one_year, partition=True)()

            # COLUMNAR
            monitor_function(c_select_all_user_informations, partition=True, partition_db=True, method="method2")()
            # monitor_function(c_raise_salary_best_moderators, partition=True, partition_db=True)()
            # monitor_function(c_look_for_the_most_common_word, partition=True, partition_db=True)()
            # monitor_function(c_most_engaged_users, partition=True, partition_db=True)()
            # monitor_function(c_get_average_age_of_users, partition=True, partition_db=True)()
            # monitor_function(c_increase_all_employee_salaries_by_10_percent_every_year, partition=True, partition_db=True)()
            monitor_function(c_bad_users, partition=True, partition_db=True, method="method2")()
            # monitor_function(c_censorship, partition=True, partition_db=True)()
            # monitor_function(c_deleting_all_user_not_connected_for_one_year, partition=True)()

def main():
    print("Starting...")

    print("Method 0 :")
    method0()
    # print("Method 1 :")
    # method1()
    # print("Method 2 :")
    # method2()
    # print("Done.")

if __name__ == '__main__':
    main()
