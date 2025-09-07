from models.user_model import Users
from flask import Flask,jsonify,request
import re

class UserController:


    @staticmethod
    def create_user():
        data=request.get_json()
        fields=['first_name','last_name','email','password','role_id']
        for key in fields:
            if key not in data:
                return jsonify({'error':'some field not found'})
        # בדיקה האם המשתמש הוא ADMIN אם לא -לא ניתן לבצע הוספת משתמש
        if data['role_id'] != 2:
            return jsonify({'error': 'Only USER (role_id=2) role can be created via API'}), 403
        # בדיקה האם אימייל חוקי
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        # בדיקה האם הסיסמא לפחות 4 תווים
        if len(data['password'])<4:
            return jsonify({'error':'password must be at least 4 characters'})
        # בדיקה שלא קיים אימייל זהה במערכת
        with Users.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = ?", (data['email'],))
            if cursor.fetchone():
                return jsonify({'error': 'Email already exists'}), 400
            cursor.close()
        result=Users.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            role_id=data['role_id'],
        )
        return jsonify(result)

    @staticmethod
    def get_all_users():
        users=Users.get_all()
        return jsonify(users)
    
    @staticmethod
    def get_user_by_id(user_id):
        user=Users.get_by_id(user_id)
        if user is None:
            return jsonify({'error':'user not found'})
        return jsonify(user)


    @staticmethod
    def login_user():
        data=request.get_json()
        email=data['email']
        password=data['password']
        user=Users.login(email,password)
        if user is None:
            return jsonify({'error':'user not found'})
        return jsonify(user)



    @staticmethod
    def delete_user(user_id):
        # בדיקת סוג משתמש -רק ADMIN יכול לבצע מחיקה
        with Users.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT role_id FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            cursor.close()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        role_id = user[0]
        if role_id != 2:
            return jsonify({'error': 'Only users with role_id=2 can be deleted via API'}), 403
        
        result=Users.delete(user_id)
        if result is None:
            return jsonify({'error':'user not found'}),404
        return jsonify(result),201

    @staticmethod
    def update_user(user_id):
        data=request.get_json()
        if not data:
           return jsonify({'error':'no data provided'})
        # בדיקת סוג משתמש -רק ADMIN יכול לבצע עדכון       
        with Users.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT role_id FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            cursor.close()
        if not row:
            return jsonify({'error': 'User not found'}), 404
        role_id = row[0]
        if role_id != 2:
            return jsonify({'error': 'Only users with role_id=2 can be updated via API'}), 403
        # בדיקה שהאימייל חוקי במידה וקיים
        if 'email' in data:
           if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
        # בדיקה האם אימייל קיים כבר במערכת
           with Users.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE email =?", (data['email'],))
                if cursor.fetchone():
                    return jsonify({'error': 'Email already in use'}), 400
                cursor.close()
        # בדיקת סיסמה תקינה-לפחות 4 תווים
        if 'password' in data:
            if len(data['password']) < 4:
                return jsonify({'error': 'Password must be at least 4 characters long'}), 400
       
        result=Users.update(user_id,**data)
        if result is None:
            return jsonify({'error':'user not found'})
        return jsonify(result),201