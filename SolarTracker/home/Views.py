from SolarTracker import app, db, firebaseDB
from flask import request, render_template, url_for, make_response, jsonify
import time
from flask_login import login_required, current_user


@app.route("/push")
def push():
    # get data from the url variable
    data = request.args
    # print it out in the terminal
    for key, value in data.items():
        print(f'{key} = {value}')
        print(f' type of key : {type(key)}')
        print(f' type of value : {type(value)}')
    # insert the data in firebase
    insertData = {
        "ldrtr": float(data["ldrtr"]),
        "ldrtl": float(data["ldrtl"]),
        "ldrbr": float(data["ldrbr"]),
        "ldrbl": float(data["ldrbl"])
    }
    # record LDR Value
    recordTime = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())
    firebaseDB.child("LDR Recorde").child(
        recordTime.replace("/", "-")).set(insertData)
    firebaseDB.child("Control").update({
        "mode": int(data["mode"]),
        "Hposi": int(data["hposi"]),
        "Vposi": int(data["vposi"])
    })
    return "done"


@app.route("/get")
def get():
    # get control child from firebase
    control = firebaseDB.child("Control").get().val()
    # print data inside it
    for key, value in control.items():
        print(f'{key} = {value}')
        print(f' type of key : {type(key)}')
        print(f' type of value : {type(value)}')
    # send response
    return f'start {control["mode"]},{control["Vposi"]},{control["Hposi"]} end.'


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # control = {"mode" : 0 , "Vposi" :"0" , "Hposi" : "0"}
    control = firebaseDB.child("Control").get().val()

    if request.method == 'POST' and request.is_json:
        print("is a post method with a json")
        req = request.get_json()

        if req.get("Hposi") or req.get("Vposi"):

            for key, value in req.items():
                # update mode
                if key == "mode":
                    firebaseDB.child("Control").update(req)
                    print("mode updated")
                # update servo position
                if key in ["Hposi", "Vposi"]:
                    print(req)
                    firebaseDB.child("Control").update(req)
                    print("position updated")
        else:
            data = firebaseDB.child(
                "LDR Recorde").order_by_key().limit_to_last(1).get()
            # extracte a dictionnary from the data returned
            for rec in data.each():
                lastRecorde = rec.val()
                print(lastRecorde)
            
            return make_response(jsonify(lastRecorde), 200)


    profile_url = url_for("static", filename='profile/'+current_user.profile)
    return render_template('home/index.html', segment='index', profile_url=profile_url,
                           Vposi=control["Vposi"], Hposi=control["Hposi"], mode=control["mode"])


# @app.route('/api', methods=['GET', 'POST'])
# def api():
#     if request.method == "POST":
#         data = firebaseDB.child(
#             "LDR Recorde").order_by_key().limit_to_last(1).get()
#         # extracte a dictionnary from the data returned
#         for rec in data.each():
#             lastRecorde = rec.val()
#             print(lastRecorde)
           

#     return make_response(jsonify(lastRecorde), 200)
