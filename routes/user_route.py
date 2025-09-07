from flask import Blueprint,jsonify,request
from controllers.user_controller import UserController

user_bp=Blueprint('users',__name__)

@user_bp.route('/users',methods=['post'])
def create_user():
    return UserController.create_user()
    
@user_bp.route('/users',methods=['GET'])
def get_all_users():
    return UserController.get_all_users()

@user_bp.route('/users/<int:user_id>',methods=['GET'])
def get_user_by_id(user_id):
    return UserController.get_user_by_id(user_id)

@user_bp.route('/login',methods=['post'])
def login_user():
    print(request.get_json())
    return UserController.login_user()

@user_bp.route('/users/<int:user_id>',methods=['delete'])
def delete_user(user_id):
    return UserController.delete_user(user_id)

@user_bp.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    return UserController.update_user(user_id)