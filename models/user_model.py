import sqlite3

class Users:
    @staticmethod
    def get_db_connection():
        return sqlite3.connect("mydb.db")
   
# יצירת טבלת משתמשים
    @staticmethod
    def create_table():
        with Users.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists users
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name Text not null,
                    last_name Text not null,
                    email Text not null,
                    password Text not null,
                    role_id INTEGER not null,
                    FOREIGN KEY (role_id) REFERENCES roles(role_id))
                '''
            cursor.execute(sql)
            cursor.close()

# הוספת משתמש
    @staticmethod
    def create(first_name,last_name,email,password,role_id):
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('''
            insert into users (first_name,last_name,email,password,role_id) values(?,?,?,?,?)
            ''',(first_name,last_name,email,password,role_id))
            user_id=cursor.lastrowid
            connection.commit()
            cursor.close()
            return{
                'user_id':user_id,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'password':password,
                'role_id':role_id
            }   

# החזרת כל המשתמשים
    @staticmethod 
    def get_all():
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from users')
            users=cursor.fetchall()
            cursor.close()
            return[
                dict(user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                password=user[4],
                role_id=user[5])for user in users
            ]

# החזרת משתמש לפי ID  
    @staticmethod
    def get_by_id(user_id):
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from users where user_id=?',(user_id,))
            user=cursor.fetchone()
            cursor.close()
            if user:
                return[
                    dict(user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                password=user[4],
                role_id=user[5])
                ]
            return None

# כניסת משתמש למערכת לפי מייל וסיסמה   
    @staticmethod
    def login(email,password):
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from users where email=? and password=?',(email,password))
            user=cursor.fetchone()
            cursor.close()
            if user:
                return[
                    dict(user_id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                password=user[4],
                role_id=user[5])
                ]
            return None

# עדכון משתמש
    @staticmethod
    def update(user_id,**kwargs):
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from users where user_id=?',(user_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            pair=""
            for key,value in kwargs.items():
                pair+=key+"="+ "'" +value+ "'" + ","
            pair=pair[:-1]
            sql=f"update users set {pair} where user_id=?"
            cursor.execute(sql,(user_id,))
            connection.commit()
            cursor.close()
            return {'message':f"user {user_id} row updated successfully"}
            
# מחיקת משתמש
    @staticmethod
    def delete(user_id):
        with Users.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('select * from users where user_id=?',(user_id,))
            if not cursor.fetchone():
                cursor.close()
                return None
            sql='delete from users where user_id=?'
            cursor.execute(sql,(user_id,))
            connection.commit()
            cursor.close()
            return{'message':f"user {user_id} row deleted successfully"}




    