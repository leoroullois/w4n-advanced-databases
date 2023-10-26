from flask import Flask, jsonify, request
from src.database import connect
from src.task3 import delete_previous_data, task3
from src.task2 import task2


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
        try:
            task3(NB_EMPLOYEES)
            response = {
                "success": True,
                "message": "Data successfully inserted into database",
                "NB_EMPLOYEES": NB_EMPLOYEES,
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

            response = {
                "success": True,
                "count": {
                    "users": users,
                    "posts": posts,
                    "comments": comments,
                    "employees": employees,
                    "departments": departments,
                    "moderators": moderators,
                },
            }
            return jsonify(response), 200
        except Exception as e:
            response = {"success": False, "message": f"An error occured: {e}"}
            return jsonify(response), 500
        finally:
            conn.close()

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
