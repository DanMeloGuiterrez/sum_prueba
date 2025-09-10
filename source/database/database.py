import mysql.connector

def obtener_conexion():

    conexion = mysql.connector.connect(
        host="sum-prueba-dmelo9918-73bf.c.aivencloud.com",    
        user="avnadmin",      
        password="AVNS_ieZU4gKGRmeMxKyaMfp",
        database="defaultdb",
        port= "11780"
        )
    return conexion