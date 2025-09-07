import sqlite3

class Likes:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("mydb.db")

# יצירת טבלת לייקים
    @staticmethod
    def create_table():
        with Likes.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists likes
                    (user_id INTEGER not null,
                    vacation_id INTEGER not null,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id)
                    )
                '''
            cursor.execute(sql)
            cursor.close()


# -Like הוספת לייק
    @staticmethod
    def create(user_id, vacation_id):
        with Likes.get_db_connection() as connection:
            cursor = connection.cursor()
            # בדוק אם המשתמש קיים
            cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
            if not cursor.fetchone():
                cursor.close()
                return {'error': 'User does not exist'}
            # בדוק אם כבר יש לייק כזה
            cursor.execute('SELECT * FROM likes WHERE user_id=? AND vacation_id=?', (user_id, vacation_id))
            if cursor.fetchone():
                cursor.close()
                return {'error': 'Like already exists for this user and vacation'}
            # (רשות) בדוק אם החופשה קיימת
            cursor.execute('SELECT * FROM vacations WHERE vacation_id=?', (vacation_id,))
            if not cursor.fetchone():
                cursor.close()
                return {'error': 'Vacation does not exist'}
            # הוסף לייק
            cursor.execute('INSERT INTO likes (user_id, vacation_id) VALUES (?, ?)', (user_id, vacation_id))
            connection.commit()
            cursor.close()
            return {
                'user_id': user_id,
                'vacation_id': vacation_id,
            }
# החזרת כל הלייקים 
    @staticmethod 
    def get_all():
        with Likes.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from likes')
            likes=cursor.fetchall()
            cursor.close()
            return[
                dict(user_id=like[0],
                vacation_id=like[1]
                )for like in likes
            ]


# החזרת כל הלייקים עם שמות
    @staticmethod
    def get_all_likes():
        with Likes.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''
            SELECT likes.user_id, users.first_name, likes.vacation_id, vacations.description
            FROM likes
            JOIN users ON likes.user_id = users.user_id
            JOIN vacations ON likes.vacation_id = vacations.vacation_id
            '''
            cursor.execute(sql)
            likes = cursor.fetchall()
            cursor.close()
        result = []
        for like in likes:
            result.append({
                'user_id': like[0],
                'username': like[1],
                'vacation_id': like[2],
                'vacation_description': like[3]
            })

        return result

# הסרת ליק-Unlike
    @staticmethod
    def delete(user_id,vacation_id):
        with Likes.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from likes where user_id=? and vacation_id=?',(user_id,vacation_id))
            if not cursor.fetchone():
                cursor.close()
                return None
            sql='delete from likes where user_id=? and vacation_id=? '
            cursor.execute(sql,(user_id,vacation_id))
            connection.commit()
            cursor.close()
            return{'message': f"Like by user {user_id} for vacation {vacation_id} deleted successfully"}



    # @staticmethod
    # def get_by_id(user_id,vacation_id):
    #     with Likes.get_db_connection() as connection:
    #         cursor=connection.cursor()
    #         cursor.execute('select * from likes where user_id=? and vacation_id=?',(user_id,vacation_id))
    #         like=cursor.fetchone()
    #         cursor.close()
    #         if like:
    #             return[
    #                 dict(user_id=like[0],
    #             vacation_id=like[1])
    #             ]
    #         return None

    
    # @staticmethod
    # def update(user_id,vacation_id):
    #     with Countries.get_db_connection() as connection:
    #         cursor=connection.cursor()
    #         cursor.execute('select * from likes where user_id=? and country_id=?',(user_id,vacation_id))
    #         if not cursor.fetchone():
    #             cursor.close()
    #             return None
    #         sql="update likes set name=? where country_id=?"
    #         cursor.execute(sql,(name,country_id))
    #         connection.commit()
    #         cursor.close()
    #         return {'message':f"country {country_id} row updated successfully"}
