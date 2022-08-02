import pymysql.cursors

class MySQLConnection:
    def __init__(self,db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root',
                                    password = '6469Mysql',
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection            #establish connection to db

    def query_db(self,query,data=None):         #method to query database
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query,data)
                print("Running Query: ",query)
                cursor.execute(query,data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid     #INSERT queries return id of the row inserted
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result               #SELECT queries return data from database as 
                                                # a list of dictionaries
                else:
                    self.connection.commit()    #UPDATE and DELETE queries will return nothing
            except Exception as e:              
                print("*************** Something went wrong ******************")
                print("***",e)
                return False                    #if the query fails, the method will return FALSE
            finally:
                self.connection.close()         #close the connection

def connectToMySQL(db):                         #this function receives database as argument,
    return MySQLConnection(db)                  #uses database to return an instance of   
                                                # MySQLConnection class
