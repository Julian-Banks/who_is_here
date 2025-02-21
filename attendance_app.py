from flask import Flask, jsonify, render_template
from attendance import attendance_list


app = Flask(__name__)

attendance_list = attendance_list()

@app.route("/")
def hello_world():
    return render_template("index.html")  # Serve an HTML page

@app.route("/data")
def get_data():
    return jsonify(attendance_list.get_present())  # Return updated data
