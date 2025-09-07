import sqlite3

class Roles:

    @staticmethod
    def get_db_connection():
        return sqlite3.connect("mydb.db")

# יצירת טבלת תפקידים
    @staticmethod
    def create_table():
        with Roles.get_db_connection() as connection:
            cursor = connection.cursor()
            sql = '''create table if not exists roles
                    (role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name Text not null)
                '''
            cursor.execute(sql)
            cursor.close()

# הוספת תפקיד לטבלה
    @staticmethod
    def create(name,):
        with Roles.get_db_connection() as connection:
            cursor=connection.cursor()
            cursor.execute('''select * from roles where name=?''',(name,))
            is_exist=cursor.fetchone()
            if is_exist:
                return None
            cursor.execute("insert into roles(name) values(?)",(name,))
            role_id = cursor.lastrowid
            connection.commit()
            cursor.close()
            return {
                'role_id': role_id,
                'name': name
            }

# החזרת כל סוגי התפקידים
    @staticmethod
    def get_all():
        with Roles.get_db_connection() as connection:
          cursor=connection.cursor()
          sql='select * from roles'
          cursor.execute(sql)
          roles=cursor.fetchall()
          cursor.close()
          return [dict(role_id=role[0],name=role[1])for role in roles]

# החזרת סוג משתמש לפי הID  
    @staticmethod
    def get_by_id(id):
        with Roles.get_db_connection() as connection:
          cursor=connection.cursor()
          sql='select * from roles where role_id=?'
          cursor.execute(sql,(id,))
          role=cursor.fetchone()
          if role:
            cursor.close()
            return [dict(role_id=role[0],name=role[1])]
          return None
          



          

    # @staticmethod
    # def delete(id):
    #     with Roles.get_db_connection() as connection:
    #       cursor=connection.cursor()
    #       sql='select * from roles where role_id=?'
    #       cursor.execute(sql, (id,))
    #       role=cursor.fetchone()
    #       if role is None:
    #         cursor.close()
    #         return None
    #       cursor.execute('delete from roles where role_id=?',(id,))
    #       connection.commit()
    #       cursor.close()
    #       return{'message': f"{id} row deleted"}

    
    # @staticmethod
    # def update(id,name):
    #     with Roles.get_db_connection() as connection:
    #       cursor=connection.cursor()
    #       sql='select * from roles where role_id=?'
    #       cursor.execute(sql, (id,))
    #       role=cursor.fetchone()
    #       if role is None:
    #         cursor.close()
    #         return None
    #       cursor.execute('update roles set name=? where role_id=?',(name,id))
    #       connection.commit()
    #       cursor.close()
    #       return{'message': f"{id} row updated to{name}  "}