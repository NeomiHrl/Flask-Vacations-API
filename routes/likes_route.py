from flask import Blueprint,jsonify,request
from controllers.likes_controller import LikesController

like_bp=Blueprint('like',__name__)

@like_bp.route('/likes',methods=['POST'])
def add_like():
    return LikesController.add_like()
    
@like_bp.route('/likes',methods=['GET'])
def get_all_likes():
    return LikesController.get_all_likes()

@like_bp.route('/likes/names',methods=['GET'])
def get_all_likes_with_names():
    return LikesController.get_all_likes_with_names()

@like_bp.route('/likes/<int:user_id>/<int:vacation_id>',methods=['delete'])
def delete_country(user_id,vacation_id):
    return LikesController.remove_like(user_id,vacation_id)
