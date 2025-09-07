import sqlite3

class Vacations:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("mydb.db")

# יצירת טבלת חופשות
    @staticmethod
    def create_table():
        with Vacations.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists vacations
                    (vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_id INTEGER not null,
                    description Text not null,
                    start_date Date not null,
                    finish_day Date not null,
                    price Real not null,
                    image_filename Text not null,
                    FOREIGN KEY (country_id) REFERENCES countries(country_id))
                '''
            cursor.execute(sql)
            cursor.close()
# הוספת חופשה   
    @staticmethod
    def create(country_id,description,start_date,finish_day,price,image_filename):
        with Vacations.get_db_connection() as connection:
            cursor = connection.cursor()
            # בדוק אם קיימת כבר חופשה עם אותם ערכים
            cursor.execute('''
                SELECT * FROM vacations WHERE country_id=? AND description=? AND start_date=? AND finish_day=? AND price=? AND image_filename=?
            ''', (country_id, description, start_date, finish_day, price, image_filename))
            if cursor.fetchone():
                cursor.close()
                return {'error': 'Vacation with these values already exists'}
            cursor.execute('''
            insert into vacations (country_id,description,start_date,finish_day,price,image_filename) values(?,?,?,?,?,?)
            ''', (country_id, description, start_date, finish_day, price, image_filename))
            vacation_id = cursor.lastrowid
            connection.commit()
            cursor.close()
            return {
                'vacation_id': vacation_id,
                'country_id': country_id,
                'description': description,
                'start_date': start_date,
                'finish_day': finish_day,
                'price': price,
                'image_filename': image_filename
            }
            
# החזרת כלל החופשות
    @staticmethod 
    def get_all():
        with Vacations.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from vacations ORDER BY start_date ASC')
            vacations=cursor.fetchall()
            cursor.close()
            return[
                dict(vacation_id=vacation[0],
                country_id=vacation[1],
                description=vacation[2],
                start_date=vacation[3],
                finish_day=vacation[4],
                price=vacation[5],
                image_filename=vacation[6]
                )for vacation in vacations
            ]

# החזרת חופשה לפי הID  
    @staticmethod
    def get_by_id(vacation_id):
        with Vacations.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from vacations where vacation_id=?',(vacation_id,))
            vacation=cursor.fetchone()
            cursor.close()
            if vacation:
                return[
                    dict(vacation_id=vacation[0],
                country_id=vacation[1],
                description=vacation[2],
                start_date=vacation[3],
                finish_day=vacation[4],
                price=vacation[5],
                image_filename=vacation[6])
                ]
            return None

# עדכון חופשה   
    @staticmethod
    def update(vacation_id,**kwargs):
        with Vacations.get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM vacations WHERE vacation_id=?', (vacation_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            # בניית ערכי העדכון
            fields = []
            values = []
            for key, value in kwargs.items():
                fields.append(f"{key} = ?")
                values.append(value)
            # בדוק אם קיימת כבר חופשה עם אותם ערכים (למעט vacation_id)
            check_fields = [key for key in kwargs.keys()]
            check_values = [kwargs[key] for key in check_fields]
            check_sql = f"SELECT * FROM vacations WHERE {' AND '.join([f'{key}=?' for key in check_fields])} AND vacation_id<>?"
            cursor.execute(check_sql, check_values + [vacation_id])
            if cursor.fetchone():
                cursor.close()
                return {'error': 'Vacation with these values already exists'}
            values.append(vacation_id)
            sql = f"UPDATE vacations SET {', '.join(fields)} WHERE vacation_id=?"
            cursor.execute(sql, values)
            connection.commit()
            cursor.close()
            return {'message': f"vacation {vacation_id} row updated successfully"}

# מחיקת חופשה 
    @staticmethod
    def delete(vacation_id):
        with Vacations.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from vacations where vacation_id=?',(vacation_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            cursor.execute('DELETE FROM likes WHERE vacation_id = ?', (vacation_id,))
            cursor.execute('DELETE FROM vacations WHERE vacation_id = ?', (vacation_id,))
            connection.commit()
            cursor.close()
            return{'message':f"vacation {vacation_id} row deleted successfully"}