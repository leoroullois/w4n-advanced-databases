from flask import Flask, jsonify, request
from src.database import connect
from src.task3 import delete_previous_data, task3
from src.task2 import task2
from src.task4 import task4
from src.task5 import task5
from src.task6 import task6


def main():
    app = Flask(__name__)

    @app.route("/task2", methods=["GET"])
    def run_task2():
        task2()
        response = {
            "success": False,
        }
        return jsonify(response), 200

    @app.route("/task3", methods=["PUT"])
    def run_task3():
        NB_EMPLOYEES = request.json["NB_EMPLOYEES"]
        NB_MANAGERS = request.json["NB_MANAGERS"]
        NB_POSTS = request.json["NB_POSTS"]
        NB_MODERATORS = request.json["NB_MODERATORS"]
        NB_COMMENTS = request.json["NB_COMMENTS"]
        NB_USERS = request.json["NB_USERS"]
        NB_CUSTOMERS = request.json["NB_CUSTOMERS"]
        NB_SELLERS = request.json["NB_SELLERS"]
        NB_HUMAN_RESOURCES = request.json["NB_HUMAN_RESOURCES"]
        NB_SALES_MODERATORS = request.json["NB_SALES_MODERATORS"]

        try:
            task3(
                NB_EMPLOYEES=NB_EMPLOYEES,
                NB_MANAGERS=NB_MANAGERS,
                NB_MODERATORS=NB_MODERATORS,
                NB_USERS=NB_USERS,
                NB_POSTS=NB_POSTS,
                NB_COMMENTS=NB_COMMENTS,
                NB_CUSTOMERS=NB_CUSTOMERS,
                NB_SELLERS=NB_SELLERS,
                NB_HUMAN_RESOURCES=NB_HUMAN_RESOURCES,
                NB_SALES_MODERATORS=NB_SALES_MODERATORS,
            )
            response = {
                "success": True,
                "message": "Data successfully inserted into database",
                "NB_EMPLOYEES": NB_EMPLOYEES,
                "NB_MANAGERS": NB_MANAGERS,
                "NB_POSTS": NB_POSTS,
                "NB_MODERATORS": NB_MODERATORS,
                "NB_COMMENTS": NB_COMMENTS,
                "NB_USERS": NB_USERS,
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500

    @app.route("/task4", methods=["PUT"])
    def run_task4():
        try:
            logs = task4()
            response = {
                "success": True,
                "message": "Data successfully inserted into database. Monitoring logs are available in the logs table.",
                "logs": logs
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500

    @app.route("/task5", methods=["GET"])
    def run_task5():
        try:
            logs = task5()
            response = {
                "success": True,
                "message": "Indexes successfully created."
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500

    @app.route("/delete", methods=["DELETE"])
    def delete_data():
        try:
            conn, curr = connect()
            delete_previous_data(conn, curr)
            response = {"success": True, "message": "Data successfully deleted"}
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500
        finally:
            conn.close()

    @app.route("/count", methods=["GET"])
    def count():
        try:
            conn, curr = connect()
            curr.execute("SELECT COUNT(*) FROM users;")
            users = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM posts;")
            posts = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM comments;")
            comments = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM employees;")
            employees = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM departments;")
            departments = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM moderation_department;")
            moderators = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM customers;")
            customers = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM human_resources_department;")
            human_resources_department = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM marketplace;")
            marketplace = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM meetings;")
            meetings = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM sales_moderation_department;")
            sales_moderation_department = curr.fetchall()[0][0]
            curr.execute("SELECT COUNT(*) FROM sellers;")
            sellers = curr.fetchall()[0][0]

            response = {
                "success": True,
                "count": {
                    "users": users,
                    "posts": posts,
                    "comments": comments,
                    "employees": employees,
                    "meetings": meetings,
                    "departments": departments,
                    "moderation_department": moderators,
                    "human_resources_department": human_resources_department,
                    "sales_moderation_department": sales_moderation_department,
                    "marketplace": marketplace,
                    "customers": customers,
                    "sellers": sellers,
                },
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500
        finally:
            conn.close()

    @app.route("/explain", methods=["GET"])
    def explain():
        try:
            conn, curr = connect()
            response = {
                "success": True,
                "cost": task6()
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500
        finally:
            conn.close()
    # task3()
    # logs = task4()
    # task5()
    task6()
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
