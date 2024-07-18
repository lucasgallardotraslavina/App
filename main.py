import sqlite3

class Comunicacion:
    def __init__(self):
        self.conexion = sqlite3.connect("db_taller.db")

    def insertar_producto(self, tipo, autor, nombre, descripcion, genero, editorial):
        cursor = self.conexion.cursor()
        db = '''INSERT INTO tabla_datos (TIPO, AUTOR, NOMBRE, DESCRIPCION, GENERO, EDITORIAL)
                VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(db, (tipo, autor, nombre, descripcion, genero, editorial))
        self.conexion.commit()
        cursor.close()

    def mostrar_producto(self):
        cursor = self.conexion.cursor()
        db = "SELECT * FROM tabla_datos"
        cursor.execute(db)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def buscar_producto(self, nombre_producto):
        cursor = self.conexion.cursor()
        db = '''SELECT * FROM tabla_datos WHERE NOMBRE = ?'''
        cursor.execute(db, (nombre_producto,))
        nombreX = cursor.fetchall()
        cursor.close()
        return nombreX

    def eliminar_productos(self, nombre):
        cursor = self.conexion.cursor()
        db = '''DELETE FROM tabla_datos WHERE NOMBRE = ?'''
        cursor.execute(db, (nombre,))
        self.conexion.commit()
        cursor.close()

    def actualizar_producto(self, ID, tipo, autor, nombre, descripcion, genero, editorial):
        cursor = self.conexion.cursor()
        db = '''UPDATE tabla_datos
                SET TIPO = ?, AUTOR = ?, NOMBRE = ?, DESCRIPCION = ?, GENERO = ?, EDITORIAL = ?
                WHERE ID = ?'''
        cursor.execute(db, (tipo, autor, nombre, descripcion, genero, editorial, ID))
        a = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return a
