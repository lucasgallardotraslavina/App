import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import loadUi
from main import Comunicacion

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('App.ui', self)

        self.bt_menu.clicked.connect(self.mover_menu)
        self.base_datos = Comunicacion()

        self.bt_restaurar.hide()

        self.bt_refrescar.clicked.connect(self.mostrar_productos)
        self.bt_agregar.clicked.connect(self.registrar_producto)
        self.bt_borrar.clicked.connect(self.eliminar_productos)
        self.bt_actualizar_tabla.clicked.connect(self.modificar_productos)
        self.bt_actualizar_buscar.clicked.connect(self.buscar_por_nombre_actualizar)
        self.bt_buscar_borrar.clicked.connect(self.buscar_por_nombre_eliminar)
        
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.frame_superior.mouseMoveEvent = self.mover_ventana

        self.bt_datos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_datos))
        self.bt_registrar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_registrar))
        self.bt_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.bt_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        
        self.tabla_borrar.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()
        
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_position = event.globalPosition().toPoint()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.click_position) 
                self.click_position = event.globalPosition().toPoint()
                event.accept()
        if event.globalPosition().toPoint().y() <= 10:
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()
        else:
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()

    def mover_menu(self):
        width = self.frame_control.width()
        normal = 0
        extender = 0
        if width == 0:
            extender = 200
        else:
            extender = normal
        self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animacion.start()
        
    def mostrar_productos(self):
        datos = self.base_datos.mostrar_producto()
        i = len(datos)
        self.tabla_productos.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.tabla_productos.setItem(tablerow,0 ,QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_productos.setItem(tablerow,1 ,QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_productos.setItem(tablerow,2 ,QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_productos.setItem(tablerow,3 ,QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_productos.setItem(tablerow,4 ,QtWidgets.QTableWidgetItem(row[5]))
            self.tabla_productos.setItem(tablerow,5 ,QtWidgets.QTableWidgetItem(row[6]))
            tablerow += 1
        self.signal_actualizar.setText("") 
        self.signal_registrar.setText("") 
        self.signal_eliminacion.setText("") 
    
    def registrar_producto(self):
        tipo = self.reg_tipo.text().upper()
        autor = self.reg_autor.text().upper()
        nombre = self.reg_nombre.text().upper()
        descripcion = self.reg_descripcion.text().upper()
        genero = self.reg_genero.text().upper()
        editorial = self.reg_editorial.text().upper()
        if tipo != '' and autor != '' and nombre != '' and descripcion != '' and genero != '' and editorial != '':
            self.base_datos.insertar_producto(tipo, autor, nombre, descripcion, genero, editorial)
            self.signal_registrar.setText('Productos Registrados')
            self.reg_tipo.clear()
            self.reg_autor.clear()
            self.reg_nombre.clear()
            self.reg_descripcion.clear()
            self.reg_genero.clear()
            self.reg_editorial.clear()
        else:
            self.signal_registrar.setText('Hay espacios vacíos')
    
    def buscar_por_nombre_actualizar(self):
        id_producto = self.act_buscar.text().upper()
        self.producto = self.base_datos.buscar_producto(id_producto)
        if len(self.producto) != 0:
            self.act_tipo.setText(self.producto[0][1])
            self.act_autor.setText(self.producto[0][2])
            self.act_nombre.setText(self.producto[0][3])
            self.act_descripcion.setText(self.producto[0][4])
            self.act_genero.setText(self.producto[0][5])
            self.act_editorial.setText(self.producto[0][6])
            self.Id = self.producto[0][0]
        else:
            self.signal_actualizar.setText("No existe")
    
    def modificar_productos(self):
        if self.producto:
            tipo = self.act_tipo.text().upper()
            autor = self.act_autor.text().upper()
            nombre = self.act_nombre.text().upper()
            descripcion = self.act_descripcion.text().upper()
            genero = self.act_genero.text().upper()
            editorial = self.act_editorial.text().upper()
            
            act = self.base_datos.actualizar_producto(self.Id, tipo, autor, nombre, descripcion, genero, editorial)
            
            if act == 1:
                self.signal_actualizar.setText("Actualizado")
                self.act_tipo.clear()
                self.act_autor.clear()
                self.act_nombre.clear()
                self.act_descripcion.clear()
                self.act_genero.clear()
                self.act_editorial.clear()
                self.act_buscar.clear()
            elif act == 0:
                self.signal_actualizar.setText("Error")
            else:
                self.signal_actualizar.setText("Incorrecto")


    def buscar_por_nombre_eliminar(self):
        nombre_producto = self.eliminar_buscar.text().upper()

        producto = self.base_datos.buscar_producto(nombre_producto)
        self.tabla_borrar.setRowCount(len(producto))

        if len(producto) == 0:
            self.signal_eliminacion.setText('No existe')
        else:
            self.signal_eliminacion.setText('Producto seleccionado')
        tablerow = 0
        for row in producto:
            self.producto_a_borrar = row[2]
            self.tabla_borrar.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_borrar.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_borrar.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_borrar.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_borrar.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[5]))
            self.tabla_borrar.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[6]))
            tablerow += 1
            
    def eliminar_productos(self):
        current_row = self.tabla_borrar.currentRow()
        
        if current_row >= 0:
            nombre_producto = self.tabla_borrar.item(current_row, 2).text()
            
            self.tabla_borrar.removeRow(current_row)
            self.base_datos.eliminar_productos(nombre_producto)


        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    mi_App = VentanaPrincipal()
    mi_App.show()
    sys.exit(App.exec())