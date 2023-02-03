from SolarTracker import app, db, firebaseDB
from flask import request, render_template, url_for, make_response, jsonify
import time
from flask_login import login_required, current_user
import requests


@app.route("/push")
def push():
    # get data from the url variable
    data = request.args
    print(data)
    # insert the data in firebase
    insertData = {
        "ldrtr": float(data["ldrtr"]),
        "ldrtl": float(data["ldrtl"]),
        "ldrbr": float(data["ldrbr"]),
        "ldrbl": float(data["ldrbl"])
    }
    # record LDR Value
    recordTime = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())
    try:
        firebaseDB.child("LDR Recorde").child(
            recordTime.replace("/", "-")).set(insertData)
    except Exception as e:
        print("fail to insert LDR Recorde !!!")
        print(e)
        return e
    # update Control Object
    try:
        firebaseDB.child("Control").update({
            "mode": int(data["mode"]),
            "Hposi": int(data["hposi"]),
            "Vposi": int(data["vposi"])
        })
    except Exception as e:
        print("fail to update Control Object!!!")
        print(e)
        return e
    return "done"


@app.route("/get")
def get():
    # get control child from firebase
    try:
        control = firebaseDB.child("Control").get().val()
        print(control)
    except requests.exceptions.ConnectionError:
        return "Check Ur connection !!"
    except requests.exceptions.ConnectTimeout:
        return "Connection Time Out"
    # send response
    return f'start {control["mode"]},{control["Vposi"]},{control["Hposi"]} end.'


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # control = {"mode" : 0 , "Vposi" :"0" , "Hposi" : "0"}
    try:
        control = firebaseDB.child("Control").get().val()
    except requests.exceptions.ConnectionError:
        return "Check Ur connection"
    except requests.exceptions.ConnectTimeout:
        return "Connection Time Out"

    # Hundel the fetch request
    if request.method == 'POST' and request.is_json:
        print("Hundel fetch Requests !")
        req = request.get_json()
        # update posi from slider value
        if req.get("Hposi") or req.get("Vposi"):
            print("Update servo Posis !")
            for key, value in req.items():
                # update servo position
                if key in ["Hposi", "Vposi"]:
                    firebaseDB.child("Control").update(req)
                    print("Position updated")

        # update mode
        elif req.get("mode") in [0, 1]:
            print("Update Mode !")
            firebaseDB.child("Control").update(req)
            print("mode updated")

        # send last LDR Recorde to dashboard
        if not req:
            print("try send last LDR recorde")
            try:
                data = firebaseDB.child(
                    "LDR Recorde").order_by_key().limit_to_last(1).get()
                # extracte a dictionnary from the data returned
                for rec in data.each():
                    lastRecorde = rec.val()
                return make_response(jsonify(lastRecorde), 200)
            except requests.exceptions.ConnectionError:
                return "Check Ur connection"
            except requests.exceptions.ConnectTimeout:
                return "Connection Time Out"

    profile_url = url_for(
        "static", filename='profile/'+current_user.profile)
    return render_template('home/index.html', segment='index', profile_url=profile_url,
                           Vposi=control["Vposi"], Hposi=control["Hposi"], mode=control["mode"])
