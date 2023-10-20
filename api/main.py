from flask import Flask, jsonify

def main():

    app = Flask(__name__)

    @app.route("/employees", methods=["GET"])
    def get_employees():
        response = {
            "success": False,
            "employees": ["Test", "Test2"],
        }
        return jsonify(response), 200

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
