import time
from src.database import connect
import src.queries

def monitor_function(func, index: bool = False, index_name: str = "btree"):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)
        print(f"Arguments: {args}, {kwargs}")
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds.")

        push_monitor_data_to_db(func.__name__, execution_time, index, index_name)
        return result

    return wrapper


def push_monitor_data_to_db(name, execution_time, index, index_name):
    conn, curr = connect()
    try:
        created_at = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())
        if index:
            curr.execute(
                f"INSERT INTO logs_index (function_name, execution_time, created_at, index_name) VALUES (%s, %s, %s, %s);",
                (name, execution_time * 1000, created_at, index_name),
            )
        else:
            curr.execute(
                f"INSERT INTO logs (function_name, execution_time, created_at) VALUES (%s, %s, %s);",
                (name, execution_time * 1000, created_at),
            )
        conn.commit()
    except Exception as e:
        print("[ERROR] Monitoring: ", e)
    finally:
        conn.close()


def extract_estimated_cost(func):
    for quer in query_list:
        with conn.cursor() as cursor:
            Read data from database
            sql = ("SELECT  EXPLAIN  FROM %s" , func.__name__) 
            cursor.execute(sql)
    

def separator(func):
    def inner(*args, **kwargs):
        print("-" * 10 +" START:" + func.__name__ + " " + "-" * 10)
        result = func(*args, **kwargs)
        print("-" * 10 +" END:" + func.__name__ + " " + "-" * 10)
        return result

    return inner

