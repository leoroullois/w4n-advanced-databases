import time
from src.database import connect

def monitor_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)
        print(f"Arguments: {args}, {kwargs}")
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds.")

        push_monitor_data_to_db(func.__name__, execution_time)
        return result

    return wrapper


def push_monitor_data_to_db(name, execution_time):
    # Push the data to the database
    conn, curr = connect()
    # timestamp with timezone
    try:
        created_at = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())
        curr.execute(
            "INSERT INTO logs (function_name, execution_time, created_at) VALUES (%s, %s, %s);",
            (name, execution_time * 1000, created_at),
        )
        conn.commit()
    except Exception as e:
        print("[ERROR] Monitoring: ", e)
    finally:
        conn.close()


def separator(func):
    def inner(*args, **kwargs):
        print("-" * 10 +" START:" + func.__name__ + " " + "-" * 10)
        result = func(*args, **kwargs)
        print("-" * 10 +" END:" + func.__name__ + " " + "-" * 10)
        return result

    return inner

