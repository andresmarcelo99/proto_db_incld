import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection

def insertVariablesIntoTable(id, Emp_id, Tipo_Producto, Date_, Ubicacion, Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='Electronics',
                                             user='root',
                                             password='Marcelosans12')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO Inventario (Id, Emp_id, Tipo_Producto, Date_, Ubicacion, Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        recordTuple = (id, Emp_id, Tipo_Producto, Date_, Ubicacion, Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        print("Record inserted successfully into Inv table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def update_data(set, where):

      connection = mysql.connector.connect(host='localhost',
                                     database='Electronics',
                                     user='root',
                                     password='Marcelosans12')

      cursor = connection.cursor()

      sql = "UPDATE Inventario SET Inventario_R = %d WHERE Id = %d" %(set, where)

      cursor.execute(sql)

      connection.commit()

      print(cursor.rowcount, "record(s) affected")


def get_next_index():

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='Electronics',
                                             user='root',
                                             password='Marcelosans12')

        sql_select_Query = "select * from Inventario"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Inventario is: ", cursor.rowcount)

        print("\nPrinting each inventory record")
        for row in records:
            print("Id = ", row[0], )
            curr = row[0]
        curr += 1

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    return curr

#insertVariablesIntoTable(get_next_index(),"mar12","botella",4/12/2020, "abd3", "12dd", "s", 22,0,0)
update_data(56,23)
