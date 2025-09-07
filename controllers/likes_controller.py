from flask import Flask,jsonify,request
from models.likes_model import Likes

class LikesController:
    @staticmethod
    def add_like():
        data=request.get_json()
        if not data or 'user_id'not in data or 'vacation_id' not in data:
            return jsonify({'error':'all fields is require'})
        result= Likes.create(data['user_id'],data['vacation_id'])
        if result:
            return jsonify(result)
        return jsonify({'error': 'could not add like'})
    
    @staticmethod
    def get_all_likes():
        likes=Likes.get_all()
        return jsonify({'likes': likes})
    
    @staticmethod
    def get_all_likes_with_names():
        likes=Likes.get_all_likes()
        return jsonify({'likes': likes})


    @staticmethod
    def remove_like(user_id,vacation_id):
        result=Likes.delete(user_id,vacation_id)
        if result is None:
            return jsonify({'error':'like row not found'}),404
        return jsonify(result)
    