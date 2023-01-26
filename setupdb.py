from SolarTracker import db , app
from SolarTracker.authentication.models import Users

with app.app_context() :
    db.drop_all()
    db.create_all()
    admin1 = Users(username = "H_Sohaib" , email = "harraoui.sohaib1@gmail.com" ,password = "sohaib" , profile ="sohaib.jpg") 
    db.session.add(admin1)
    db.session.commit()