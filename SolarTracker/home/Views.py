from SolarTracker import app, db, firebaseDB
from flask import request, render_template, url_for, make_response, jsonify
import time
from flask_login import login_required, current_user
import requests
from werkzeug.datastructures import ImmutableMultiDict
ldrRecorde = {
    "ldrtr": 1,
    "ldrtl": 1,
    "ldrbr": 1,
    "ldrbl": 1
}


@app.route("/push")
def push():
    # get data from the url variable
    data = request.args.to_dict(flat=True)  # data is a dict
    # print(data)
    if data.__len__() == 2:  # push servo position AUTO_MODE
        try:
            firebaseDB.child("Control").update({
                "Hposi": int(data.get("hposi")),
                "Vposi": int(data.get("vposi"))
            })
        except requests.exceptions.ConnectionError:
            return "Check Ur connection"
        except requests.exceptions.ConnectTimeout:
            return "Connection Time Out"
        except Exception as e:
            print(e)
            return "unexpected error occurred !!"

    elif data.__len__() > 2:  # push LDR & Power recorde 'OUT of any MODE'
        # insert Power Recordes
        try:
            firebaseDB.child("Power").child(
                time.strftime("%d-%m-%Y", time.localtime())).child(time.strftime("%H:%M:%S", time.localtime())).set(
                {"courant": data.get("courant"),
                 "tension": data.get("tension")})
        except requests.exceptions.ConnectionError:
            return "Check Ur connection"
        except requests.exceptions.ConnectTimeout:
            return "Connection Time Out"
        except Exception as e:
            print(e)
            return "unexpected error occurred !!"
        #  LDR Recordes
        global ldrRecorde
        ldrRecorde = {
            "ldrtr": int(data.get("ldrtr")),
            "ldrtl": int(data.get("ldrtl")),
            "ldrbr": int(data.get("ldrbr")),
            "ldrbl": int(data.get("ldrbl"))
        }
        print(ldrRecorde)

    return "done"


@app.route("/get")
def get():
    # get control child from firebase
    try:
        control = firebaseDB.child("Control").get().val()
        # print(control)
    except requests.exceptions.ConnectionError:
        return "Check Ur connection !!"
    except requests.exceptions.ConnectTimeout:
        return "Connection Time Out"
    except Exception as e:
        print(e)
        return "unexpected error occurred !!"
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
    except Exception as e:
        print(e)
        return "unexpected error occurred !!"

  # # Hundel the fetch request
    if request.method == 'POST' and request.is_json:
        # print("Hundel fetch Requests !")
        req = request.get_json()
        # update posi from slider value
        if req.get("Hposi") or req.get("Vposi"):
            for key, value in req.items():
                if key in ["Hposi", "Vposi"]:
                    try:
                        firebaseDB.child("Control").update(req)
                        print("Position updated")
                    except requests.exceptions.ConnectionError:
                        return "Check Ur connection"
                    except requests.exceptions.ConnectTimeout:
                        return "Connection Time Out"
                    except Exception as e:
                        print(e)
                        return "unexpected error occurred !!"

        # update mode
        elif req.get("mode") in [0, 1]:
            print("Update Mode !")
            try:
                firebaseDB.child("Control").update(req)
                print("mode updated !")
            except requests.exceptions.ConnectionError:
                return "Check Ur connection"
            except requests.exceptions.ConnectTimeout:
                return "Connection Time Out"
            except Exception as e:
                print(e)
                return "unexpected error occurred !!"

        # send last LDR Recorde to dashboard
        if not req:  # empty json
            print("try send last LDR recorde")
            refreshedData = ldrRecorde
            refreshedData["Hposi"] = control.get("Hposi")
            refreshedData["Vposi"] = control.get("Vposi")
            refreshedData["mode"] = control.get("mode")
            print(refreshedData)
            return make_response(jsonify(refreshedData), 200)
    # for the account profile
    profile_url = url_for(
        "static", filename='profile/'+current_user.profile)
    return render_template('home/index.html', segment='index', profile_url=profile_url, mode=control["mode"])


@app.route('/index/tables')
@login_required
def tables():
    try:
        data = dict(firebaseDB.child("Power").get().val())
    except requests.exceptions.ConnectionError:
        return "Check Ur connection"
    except requests.exceptions.ConnectTimeout:
        return "Connection Time Out"
    except Exception as e:
        print(e)
        return "unexpected error occurred !!"

    print(data)
#   # for debuging !
    # for key1, value1 in data.items():
    #     print("******************************")
    #     print(key1)
    #     print(value1)
    #     for key2, value2 in value1.items():
    #         print(key2)
    #         print(value2)
    profile_url = url_for("static", filename='profile/'+current_user.profile)
    return render_template('home/tables-data.html', profile_url=profile_url, data=data)
