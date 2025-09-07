from flask import Flask
from models.country_model import Countries
from models.likes_model import Likes
from models.role_model import Roles
from models.user_model import Users
from models.vacation_model import Vacations
from routes.role_route import role_bp
from routes.user_route import user_bp
from routes.country_route import country_bp
from routes.vacations_route import vacation_bp
from routes.likes_route import like_bp
from flask_cors import CORS


app=Flask(__name__)
CORS(app)

app.register_blueprint(role_bp)
app.register_blueprint(user_bp)
app.register_blueprint(country_bp)
app.register_blueprint(vacation_bp)
app.register_blueprint(like_bp)


# יצירת טבלאות 

Countries.create_table()
Likes.create_table()
Users.create_table()
Vacations.create_table()
Roles.create_table()



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

