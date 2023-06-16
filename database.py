#conding:utf-8
import sqlite3
import asyncio

class Users:
    def __init__(self):
        self.database = "database.db"
        self.conn = sqlite3.connect(self.database)
        self.curs = self.conn.cursor()

    async def createUser(self, name_user:str, last_name_user:str, id_telegram:int) ->bool:
        try:
            new_user = (self.curs.lastrowid, name_user, last_name_user, id_telegram)
            self.curs.execute('INSERT INTO data10_users VALUES(?, ?, ?, ?)', new_user)
            self.conn.commit()
            return True
        except Exception as error:
            print(error)
            return False
        finally:
            self.conn.close()

    async def searchUser(self, id_telegram: int) ->tuple:
        try:
            id_telegram = (id_telegram,)
            result_user = self.curs.execute("SELECT * FROM data10_users WHERE id_telegram = ?", id_telegram)
            return result_user.fetchone()
        except:
            return False
        finally:
            self.conn.close()

if __name__ == '__main__':
    user = Users()
    response = asyncio.run(user.createUser("Josh", "Sublime", 981900910))
    print(response)

