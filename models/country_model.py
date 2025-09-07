import sqlite3

class Countries:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("mydb.db")

# יצירת טבלת מדינות
    @staticmethod
    def create_table():
        with Countries.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists countries
                    (country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name Text not null)
                '''
            cursor.execute(sql)
            cursor.close()

# הוספת מדינה חדשה
    @staticmethod
    def create(name):
        with Countries.get_db_connection() as connection:
            cursor = connection.cursor()
            # בדוק אם המדינה כבר קיימת
            cursor.execute('SELECT * FROM countries WHERE name=?', (name,))
            if cursor.fetchone():
                cursor.close()
                return {'error': 'Country with this name already exists'}
            cursor.execute('''
            insert into countries (name) values(?)
            ''', (name,))
            country_id = cursor.lastrowid
            connection.commit()
            cursor.close()
            return {
                'country_id': country_id,
                'name': name,
            }

# החזרת כל המדינות
    @staticmethod 
    def get_all():
        with Countries.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from countries')
            countries=cursor.fetchall()
            cursor.close()
            return[
                dict(country_id=country[0],
                name=country[1]
                )for country in countries
            ]

# החזרת מדינה לפי ID
    @staticmethod
    def get_by_id(country_id):
        with Countries.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from countries where country_id=?',(country_id,))
            country=cursor.fetchone()
            cursor.close()
            if country:
                return[
                    dict(country_id=country[0],
                name=country[1])
                ]
            return None

# עדכון מדינה
    @staticmethod
    def update(country_id,name):
        with Countries.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from countries where country_id=?',(country_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            sql="update countries set name=? where country_id=?"
            cursor.execute(sql,(name,country_id))
            connection.commit()
            cursor.close()
            return {'message':f"country {country_id} row updated successfully"}

# מחיקת מדינה מהטבלה
    @staticmethod
    def delete(country_id):
        with Countries.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from countries where country_id=?',(country_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            sql='delete from countries where country_id=?'
            cursor.execute(sql,(country_id,))
            connection.commit()
            cursor.close()
            return{'message':f"country {country_id} row deleted successfully"}
