from flask import Flask, jsonify, render_template, request
from attendance import attendance_list


app = Flask(__name__)

attendance_list = attendance_list()

@app.route("/")
def hello_world():
    return render_template("index.html")  # Serve an HTML page

@app.route("/data")
def get_data():
    return jsonify(attendance_list.get_present())  # Return updated data


@app.route("/update_attendance", methods=['POST'])
def update_attendance():
    data = request.json
    name = data['name']
    drill_attendance = data['drill_attendance']

    success = attendance_list.update_drill_attendance(name, drill_attendance)
    
    if success:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failure", "reason": "Unable to update drill_attendance"}), 404