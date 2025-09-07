from flask import Flask,jsonify,request
from models.country_model import Countries

class CountryController:
    @staticmethod
    def create_country():
        data=request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error':'name is require'})
        result= Countries.create(data['name'])
        if result:
            return jsonify(result)
        return jsonify({'error': 'could not create country'})
    
    @staticmethod
    def get_all_countries():
        countries=Countries.get_all()
        return jsonify({'countries': countries})
    

    @staticmethod
    def get_country_by_id(id):
        country=Countries.get_by_id(id)
        return jsonify({'country': country})
    

    
    @staticmethod
    def delete_country(country_id):
        result=Countries.delete(country_id)
        if result is None:
            return jsonify({'error':'country not found'}),404
        return jsonify(result)
    
    
    @staticmethod
    def update_country(country_id):
        data=request.get_json()
        if not data:
           return jsonify({'error':'no data provided'})
        result=Countries.update(country_id,(data['name']))
        if result is None:
            return jsonify({'error':'country_id not found'}),404
        return jsonify(result)
    
    
