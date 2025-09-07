from models.vacation_model import Vacations
from flask import Flask,jsonify,request
from datetime import datetime


class VacationController:
    
    @staticmethod
    def create_vacation():
        data=request.get_json()
        fields=['country_id','description','start_date','finish_day','price','image_filename']
        for key in fields:
            if key not in data:
                return jsonify({'error':'some field not found'})
        # בדיקה האם המחיר בין 0 ל10000
        if data['price']<0 or data['price']>10000:
            return jsonify({'error':'price must be between 0 to 10000'})
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        finish_day = datetime.strptime(data['finish_day'], "%Y-%m-%d")
        # בדיקה האם יום ההתחלה מוקדם מיום הסיום
        if start_date > finish_day:
            return jsonify({'error':'finish_day must be later than start_date'})
        today=datetime.today()
        # בדיקה האם התאריך הוא עתידי
        if start_date <today:
            return jsonify({'error':'the date cant be past'})
        result=Vacations.create(
            country_id=data['country_id'],
            description=data['description'],
            start_date=data['start_date'],
            finish_day=data['finish_day'],
            price=data['price'],
            image_filename=data['image_filename']
        )
        return jsonify(result)

    @staticmethod
    def get_all_vacations():
        vacations=Vacations.get_all()
        return jsonify(vacations)
    
    @staticmethod
    def get_vacation_by_id(vacation_id):
        vacation=Vacations.get_by_id(vacation_id)
        if vacation is None:
            return jsonify({'error':'vacation not found'})
        return jsonify(vacation)

    @staticmethod
    def update_vacation(vacation_id):
        data=request.get_json()
        fields=['country_id','description','start_date','finish_day','price']
        for key in fields:
            if key not in data:
                return jsonify({'error':'all fields is required'})
        price = data['price']
        if price < 0 or price > 10000:
             return jsonify({'error': 'price must be between 0 and 10000'}), 400
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        finish_day = datetime.strptime(data['finish_day'], "%Y-%m-%d")
        if start_date > finish_day:
            return jsonify({'error':'finish_day must be later than start_date'})
        result=Vacations.update(vacation_id,**data)
        if result is None:
            return jsonify({'error':'vacation_id not found'}),404
        return jsonify(result)

    @staticmethod
    def delete_vacation(vacation_id):
        result=Vacations.delete(vacation_id)
        if result is None:
            return jsonify({'error':'vacation not found'}),404
        return jsonify(result),201