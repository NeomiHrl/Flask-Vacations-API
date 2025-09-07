from flask import Flask,jsonify,request
from models.role_model import Roles

class RoleController:
    @staticmethod
    def create_role():
        data=request.get_json()
        if not data:
            return jsonify({'error':'name is require'})
        result= Roles.create(data['name'])
        if result:
            return jsonify(result)
        return jsonify({'error':'role already exist'})

    @staticmethod
    def get_all_roles():
        roles=Roles.get_all()
        return jsonify({'roles': roles})
    

    @staticmethod
    def get_role_by_id(id):
        role=Roles.get_by_id(id)
        if role is None:
            return jsonify({'error':'role not found'})
        return jsonify({'role': role})
    

    
    @staticmethod
    def delete_role(role_id):
        result=Roles.delete(role_id)
        if result is None:
            return jsonify({'error':'role not found'}),404
        return jsonify(result)
    
    
    @staticmethod
    def update_role(role_id):
        data=request.get_json()
        result=Roles.update(role_id,(data['name']))
        if result is None:
            return jsonify({'error':'id_role not found'}),404
        return jsonify(result)    

    
