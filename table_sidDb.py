import mysql.connector
from mysql.connector import MySQLConnection, Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='Electronics',
                                         user='root',
                                         password='Marcelosans12')

    mySql_Create_Table_Query = """CREATE TABLE Inventario (
                             Id int(250) NOT NULL,
                             Emp_id varchar(250) NOT NULL,
                             Tipo_Producto varchar(50) NOT NULL,
                             Date_ Date NOT NULL,
                             Ubicacion varchar(250) NOT NULL,
                             Codigo varchar(250) NOT NULL,
                             Descripcion varchar(250) NOT NULL,
                             Inventario_T int(250) NOT NULL,
                             Inventario_R int(250) NOT NULL,
                             Diferencia int(250) NOT NULL,
                             PRIMARY KEY (Id)) """

    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Inv Table created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
