import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, 
    QHeaderView, QStackedLayout, QLabel, QLineEdit, QMessageBox, QInputDialog, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Botones(QWidget):
    """Clase del Layout de botones principales"""
    def __init__(self, stack_layout, dinero):
        super().__init__()
        self.stack_layout = stack_layout

        # Crear botones con colores
        self.boton_venta = QPushButton("Venta")
        self.boton_venta.setStyleSheet("background-color: lightgreen; color: black;")
        self.boton_venta.clicked.connect(lambda: self.stack_layout.setCurrentIndex(2))  # Cambiar a pantalla de venta

        self.boton_inventario = QPushButton("Inventario")
        self.boton_inventario.setStyleSheet("background-color: yellow; color: black;")
        self.boton_inventario.clicked.connect(lambda: self.stack_layout.setCurrentIndex(0))

        self.boton_ganancias = QPushButton(f"Pedido")
        self.boton_ganancias.setStyleSheet("background-color: pink; color: black;")

        # Ajustar fuente y hacer los botones responsivos
        for boton in [self.boton_venta, self.boton_inventario, self.boton_ganancias]:
            boton.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Diseño vertical para los botones
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 15, 20, 15)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.boton_venta)
        self.layout.addWidget(self.boton_inventario)
        self.layout.addWidget(self.boton_ganancias)
        self.layout.addWidget(dinero)
        self.layout.addStretch()
        # -- TO DO --
        #self.setAutoFillBackground(True)                   
        #self.setStyleSheet("background-color: #ADD8E6;")  

        self.setLayout(self.layout)

class Inventario(QWidget):
    """Clase del Layout del inventario"""
    def __init__(self, tabla, usuario):
        super().__init__()
        self.usuario = usuario
        # Layout principal (vertical)
        self.layout_inventario = QVBoxLayout()
        self.layout_inventario.setContentsMargins(25, 25, 25, 25)
        self.layout_inventario.setSpacing(10)

        # Crear la tabla y guardarla en una variable
        self.tabla = tabla

        # Layout de botones (vertical)
        self.layout_botones = QVBoxLayout()
        self.layout_botones.setContentsMargins(10, 10, 10, 10)
        self.layout_botones.setSpacing(10)

        # Agregar
        self.boton_agregar = QPushButton("Agregar item")
        self.boton_agregar.setStyleSheet("background-color: pink; color: black;")
        self.boton_agregar.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.boton_agregar.clicked.connect(self.mostrar_agregar_producto)
        self.layout_botones.addWidget(self.boton_agregar)

        # Elminimar
        self.boton_eliminar = QPushButton("Eliminar item")
        self.boton_eliminar.setStyleSheet("background-color: lightcoral; color: black;")
        self.boton_eliminar.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.boton_eliminar.clicked.connect(self.eliminar_producto)  # Conectar al método eliminar
        self.layout_botones.addWidget(self.boton_eliminar)

        # Modificar
        self.boton_modificar = QPushButton("Modificar item")
        self.boton_modificar.setStyleSheet("background-color: lightyellow; color: black;")
        self.boton_modificar.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.boton_modificar.clicked.connect(self.mostrar_modificar_producto)
        self.layout_botones.addWidget(self.boton_modificar)

        # Para ventanas pequeñas
        self.layout_botones.addStretch()
        self.boton_agregar.setMinimumHeight(80)
        self.boton_eliminar.setMinimumHeight(80)
        self.boton_modificar.setMinimumHeight(80)

        # Layout contenedor
        contenedor_botones = QWidget()
        contenedor_botones.setLayout(self.layout_botones)
   
        self.layout_inventario.addWidget(self.tabla)  # Agrega la tabla
        self.layout_inventario.addWidget(contenedor_botones)  # Agrega los botones

        # Distribuir el espacio con porcentajes
        self.layout_inventario.setStretchFactor(self.tabla, 8) 
        self.layout_inventario.setStretchFactor(contenedor_botones, 2) 

        self.setLayout(self.layout_inventario)


    def mostrar_agregar_producto(self):
        """Crear la ventana de agregar producto"""
        if self.usuario == "admn":
            self.agregar_producto = AgregarProducto(self.tabla)
            self.agregar_producto.setWindowTitle("Agregar Producto")
            self.agregar_producto.show()
        else:
            QMessageBox.warning(self, "Error", "Permiso denegado")

    def eliminar_producto(self):
        """Eliminar el producto seleccionado de la tabla y del archivo, con confirmación"""
        if self.usuario == "admn":
            row = self.tabla.table.currentRow()
            if row != -1:  # Se tiene que elegir una fila
                respuesta = QMessageBox.question(self, 'Confirmación', 
                                                '¿Estás seguro de que quieres eliminar este producto?',
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if respuesta == QMessageBox.StandardButton.Yes:
                    del self.tabla.products[row]
                    self.tabla.table.removeRow(row)
                    self.tabla.guardarArchivos()
                    self.tabla.actualizarTabla()
                    print("Producto eliminado correctamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                print("No se ha seleccionado ningún producto.")
        else:
            QMessageBox.warning(self, "Error", "Permiso denegado")

    def mostrar_modificar_producto(self):
        #print(self.usuario)
        """Abrir ventana para modificar el producto seleccionado"""
        if self.usuario == "admn":
            row = self.tabla.table.currentRow()
            if row != -1:  # Se tiene que elegir una fila
                producto = self.tabla.products[row]
                # Ventana con los datos del producto
                self.modificar_producto = ModificarProducto(self.tabla, row, producto)
                self.modificar_producto.setWindowTitle("Modificar Producto")
                self.modificar_producto.show()
            else:
                QMessageBox.warning(self, "Error", "Selecciona un producto para modificar.")
        else:
            QMessageBox.warning(self, "Error", "Permiso denegado")

class Tabla(QWidget):
    """Clase para la tabla de inventario"""
    def __init__(self):
        super().__init__()

        self.file_name = "inventario.txt"  # Nombre del archivo txt
        self.products = []  # Lista para almacenar los productos
        self.cargarArchivos()

        # Crear la tabla
        self.table = QTableWidget(len(self.products), 4)  # 4 columnas: ID, Nombre, Stock, Precio
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Stock", "Precio"])
        self.table.setStyleSheet("background-color: lightgray; color: black;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Llenar la tabla con los productos leídos
        self.actualizarTabla()

        # Layout para la tabla
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def cargarArchivos(self):
        """Lee los productos del archivo de texto e inicializa la lista de productos"""
        try:
            with open(self.file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    # Asumimos que cada línea tiene el formato id,nombre,stock,precio
                    data = line.strip().split(",")
                    if len(data) == 4:
                        self.products.append(data)
        except FileNotFoundError:
            print(f"El archivo {self.file_name} no existe. Se creará uno nuevo.")

    def actualizarTabla(self):
        """Llena la tabla con los datos de los productos"""
        self.table.setRowCount(0)  # Eliminar todas las filas actuales
        for row, product in enumerate(self.products):
            self.table.insertRow(row)
            for col, value in enumerate(product):
                self.table.setItem(row, col, QTableWidgetItem(value))

    def guardarArchivos(self):
        """Guarda la lista de productos actualizada al archivo"""
        with open(self.file_name, "w") as file:
            for product in self.products:
                file.write(",".join(product) + "\n")

class AgregarProducto(QWidget):
    """Clase para el boton de agregar"""
    def __init__(self, tabla):
        super().__init__()

        self.tabla = tabla  # Recibimos la instancia de la tabla

        # Layout para la pantalla de agregar producto
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Crear los campos de entrada
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del producto (Código de barras)")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del producto")
        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Cantidad en stock")
        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Precio por unidad")

        # Botón para guardar el producto
        self.boton_guardar = QPushButton("Guardar Producto")
        self.boton_guardar.setStyleSheet("background-color: lightgreen; color: black;")
        self.boton_guardar.clicked.connect(self.guardar_producto)

        # Añadir los elementos al layout
        self.layout.addWidget(self.input_id)
        self.layout.addWidget(self.input_nombre)
        self.layout.addWidget(self.input_stock)
        self.layout.addWidget(self.input_precio)
        self.layout.addWidget(self.boton_guardar)

        self.setLayout(self.layout)

    def guardar_producto(self):
        """Guarda el nuevo producto en el archivo de texto y actualiza la tabla"""
        id_producto = self.input_id.text()
        nombre_producto = self.input_nombre.text()
        stock_producto = self.input_stock.text()
        precio_producto = self.input_precio.text()

        # Validar que los campos no estén vacíos
        if id_producto and nombre_producto and stock_producto and precio_producto:
            # Buscar si el producto ya existe en el inventario
            producto_existente = None
            for product in self.tabla.products:
                if product[0] == id_producto:
                    producto_existente = product
                    break

            if producto_existente:
                # Si el producto existe, actualizamos el stock
                producto_existente[2] = str(int(producto_existente[2]) + int(stock_producto))
                print(f"Stock actualizado para {producto_existente[1]}")
            else:
                # Si el producto no existe, lo agregamos como nuevo
                nuevo_producto = [id_producto, nombre_producto, stock_producto, precio_producto]
                self.tabla.products.append(nuevo_producto)
                print("Producto agregado como nuevo.")

            # Guardar los productos en el archivo
            self.tabla.guardarArchivos()

            # Actualizar la tabla
            self.tabla.actualizarTabla()

            # Limpiar los campos
            self.input_id.clear()
            self.input_nombre.clear()
            self.input_stock.clear()
            self.input_precio.clear()
            print("Producto guardado correctamente.")
        else:
            print("Todos los campos deben ser completos.")

class ModificarProducto(QWidget):
    """Clase para modificar un producto en la tabla."""
    def __init__(self, tabla, row, producto):
        super().__init__()

        self.tabla = tabla
        self.row = row
        self.producto = producto

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Layout para formulario (etiquetas + inputs)
        form_layout = QFormLayout()

        # Crear los campos de entrada con sus etiquetas
        self.input_id = QLineEdit(self.producto[0])
        self.input_nombre = QLineEdit(self.producto[1])
        self.input_stock = QLineEdit(self.producto[2])
        self.input_precio = QLineEdit(self.producto[3])

        # Agregar etiquetas e inputs al formulario
        form_layout.addRow(QLabel("ID del Producto:"), self.input_id)
        form_layout.addRow(QLabel("Nombre:"), self.input_nombre)
        form_layout.addRow(QLabel("Stock:"), self.input_stock)
        form_layout.addRow(QLabel("Precio:"), self.input_precio)

        for input_box in [self.input_id, self.input_nombre, self.input_precio, self.input_stock]:
            input_box.setFont(QFont("Arial", 15))  # Aumentar tamaño de fuente
            input_box.setFixedSize(200, 40)  # Ajustar tamaño de los inputs
            input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar texto

        # Botón para guardar cambios
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet("background-color: lightgreen; color: black;")
        self.boton_guardar.clicked.connect(self.guardar_cambios)

        # Agregar todo al layout principal
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.boton_guardar)
        self.setLayout(self.layout)

    def guardar_cambios(self):
        """Guardar los cambios en el producto en el archivo txt"""
        id_producto = self.input_id.text()
        nombre_producto = self.input_nombre.text()
        stock_producto = self.input_stock.text()
        precio_producto = self.input_precio.text()

        # Validar que los campos no estén vacíos
        if id_producto and nombre_producto and stock_producto and precio_producto:
            # Actualizar el producto en la lista
            self.tabla.products[self.row] = [id_producto, nombre_producto, stock_producto, precio_producto]

            # Guardar los cambios en el archivo
            self.tabla.guardarArchivos()

            # Actualizar la tabla
            self.tabla.actualizarTabla()

            # Cerrar la ventana
            self.close()
            print("Producto modificado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos deben ser completos.")

class InputCodigo(QWidget):
    """Clase para el input de la venta"""
    def __init__(self):
        super().__init__()

        # Crear layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Crear el label y el input
        label = QLabel("Ingrese Código:")
        label.setFont(QFont("Arial", 24, QFont.Weight.Bold))  # Texto más grande
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto

        self.input_codigo = QLineEdit()
        self.input_codigo.setFont(QFont("Arial", 30))  # Hacer el input más grande
        self.input_codigo.setFixedSize(400, 80)  # Ajustar tamaño del input
        self.input_codigo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar texto dentro del input

        # Agregar los elementos al layout
        self.layout.addStretch()
        self.layout.addWidget(label)
        self.layout.addWidget(self.input_codigo, alignment=Qt.AlignmentFlag.AlignCenter)  # Centrar input
        self.layout.addStretch()  # Espaciador inferior

        self.setLayout(self.layout)

class Venta(QWidget):
    """Layout principal de la venta"""
    def __init__(self, tabla, dinero):
        super().__init__()

        self.tabla = tabla  # Asegúrate de que está sea la unica insatancia de la tabla
        self.dinero = dinero # Instancia de Dinero
        self.venta_total = 0
        
        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Crear la tabla del carrito
        self.carrito = QTableWidget(0, 3)  # 0 filas iniciales, 3 columnas
        self.carrito.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio"])
        self.carrito.setStyleSheet("background-color: lightgray; color: black;")
        self.carrito.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.carrito.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Crear el input de código
        self.input_codigo = QLineEdit()
        self.input_codigo.setFont(QFont("Arial", 20))
        self.input_codigo.setPlaceholderText("Ingrese el código del producto")
        self.input_codigo.setFixedSize(400, 50)
        self.input_codigo.returnPressed.connect(self.agregar_al_carrito)  # Conectar al presionar Enter

        # Crear el QLabel para mostrar el total de la venta
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Crear botones
        self.boton_eliminar = QPushButton("Eliminar item")
        self.boton_eliminar.setStyleSheet("background-color: lightcoral; color: black;")
        self.boton_eliminar.clicked.connect(self.eliminar_del_carrito)

        self.boton_terminar = QPushButton("Terminar venta")
        self.boton_terminar.setStyleSheet("background-color: lightgreen; color: black;")
        self.boton_terminar.clicked.connect(self.terminar_venta)

        # Crear un QHBoxLayout para el input de código y el total
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_codigo)
        input_layout.addWidget(self.total_label)

        # Layout de botones
        boton_layout = QHBoxLayout()
        boton_layout.addWidget(self.boton_eliminar)
        boton_layout.addWidget(self.boton_terminar)

        # Agregar widgets al layout
        self.layout.addWidget(self.carrito)
        self.layout.addLayout(input_layout)
        self.layout.addLayout(boton_layout)

        self.setLayout(self.layout)

    def agregar_al_carrito(self):
        """Función luego del input del código"""
        codigo = self.input_codigo.text()
        if codigo:
            # Buscar el producto en el inventario
            producto_encontrado = None
            for product in self.tabla.products:
                if product[0] == codigo:
                    producto_encontrado = product
                    break

            if producto_encontrado:
                # Pedir la cantidad
                cantidad, ok = QInputDialog.getInt(self, "Cantidad", "Ingrese la cantidad de productos", 1, 1, 100, 1)
                if ok and cantidad > 0:
                    # Verificar que haya suficiente stock
                    stock_disponible = int(producto_encontrado[2])
                    if cantidad <= stock_disponible:
                        # Agregar el producto al carrito
                        precio = float(producto_encontrado[3])
                        fila = self.carrito.rowCount()
                        self.carrito.insertRow(fila)
                        self.carrito.setItem(fila, 0, QTableWidgetItem(producto_encontrado[1]))  # Nombre del producto
                        self.carrito.setItem(fila, 1, QTableWidgetItem(str(cantidad)))  # Cantidad
                        self.carrito.setItem(fila, 2, QTableWidgetItem(f"${precio:.2f}"))  # Precio

                        # Guardar los cambios en el archivo
                        self.tabla.guardarArchivos()

                        # Limpiar el input de código
                        self.input_codigo.clear()

                        # Actualizar el total
                        self.actualizar_total(precio * cantidad)

                    else:
                        QMessageBox.warning(self, "Stock insuficiente", "No hay suficiente stock para esta cantidad.")
                else:
                    QMessageBox.warning(self, "Cantidad inválida", "Por favor, ingrese una cantidad válida.")
            else:
                QMessageBox.warning(self, "Producto no encontrado", "El producto con el código ingresado no se encuentra en el inventario.")

    def eliminar_del_carrito(self):
        """Eliminar el producto seleccionado del carrito"""
        fila = self.carrito.currentRow()
        if fila != -1:  # Si hay una fila seleccionada
            producto_nombre = self.carrito.item(fila, 0).text()
            cantidad = int(self.carrito.item(fila, 1).text())

            # Eliminar la fila del carrito
            self.carrito.removeRow(fila)

            # Guardar los cambios en el archivo
            self.tabla.guardarArchivos()

            # Actualizar el total
            self.actualizar_total(-(producto_nombre * cantidad))

    def terminar_venta(self):
        """Reiniciamos el carrito y actualizamos el inventario"""
        if self.carrito.rowCount() == 0:
            QMessageBox.warning(self, "Carrito vacío", "No hay productos en el carrito.")
            return

        # Recorrer los productos en el carrito
        for row in range(self.carrito.rowCount()):
            nombre_producto = self.carrito.item(row, 0).text()
            cantidad_vendida = int(self.carrito.item(row, 1).text())

            # Buscar el producto en el inventario
            for product in self.tabla.products:
                if product[1] == nombre_producto:  # Comparar por nombre
                    stock_actual = int(product[2])  # Stock actual
                    nuevo_stock = stock_actual - cantidad_vendida  # Reducir stokc

                    if nuevo_stock < 0:
                        QMessageBox.warning(self, "Error", f"Stock insuficiente para {nombre_producto}.")
                        return
                    
                    product[2] = str(nuevo_stock)  # Actualizar el stock en la lista

        # Guardar cambios en el archivo
        self.tabla.guardarArchivos()

        # Refrescar la tabla del inventario
        self.tabla.actualizarTabla()

        # Limpiar el carrito
        self.carrito.setRowCount(0)
        self.total_label.setText("Total: $0.00")

        # Agregar el dinero a la caja
        self.dinero.actualizar_dinero(self.venta_total)
        self.venta_total = 0
        

        QMessageBox.information(self, "Venta completada", "La venta se ha registrado correctamente.")
        

    def actualizar_total(self, valor):
        """Actualiza el total de la venta en el QLabel"""
        self.venta_total += valor

        # Actualizar el texto del total en la etiqueta
        self.total_label.setText(f"Total: ${self.venta_total:.2f}")

class Dinero(QWidget):
    """Clase para mostrar el dinero total en caja y guardado"""
    def __init__(self):
        super().__init__()

        self.archivo = "dinero.txt"

        # Cargar dinero desde el archivo
        self.dinero_caja, self.dinero_guardado = self.cargar_dinero()

        self.layout = QVBoxLayout()

        self.label_caja = QLabel(f"Dinero en caja:")
        self.label_caja.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        self.label_caja_dinero = QLabel(f"${self.dinero_caja:.2f}")
        self.label_caja_dinero.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        self.boton_retirar = QPushButton("Retirar dinero")
        self.boton_retirar.setFont(QFont("Arial", 14))
        self.boton_retirar.clicked.connect(self.retirar_dinero_popup)

        self.label_guardado = QLabel(f"Dinero guardado:")
        self.label_guardado.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        self.label_guardado_dinero = QLabel(f"${self.dinero_guardado:.2f}")
        self.label_guardado_dinero.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        # Botón para guardar dinero
        self.boton_guardar = QPushButton("Guardar Dinero")
        self.boton_guardar.setFont(QFont("Arial", 14))
        self.boton_guardar.clicked.connect(self.guardar_dinero_popup)

        self.layout.addWidget(self.label_caja)
        self.layout.addWidget(self.label_caja_dinero)
        self.layout.addWidget(self.boton_retirar)
        self.layout.addWidget(self.label_guardado)
        self.layout.addWidget(self.label_guardado_dinero)
        self.layout.addWidget(self.boton_guardar)
        
        self.setLayout(self.layout)

    def actualizar_dinero(self, monto):
        """Añade dinero a la caja, actualiza los labels y guarda los datos"""
        self.dinero_caja += monto
        self.label_caja_dinero.setText(f"${self.dinero_caja:.2f}")
        self.guardar_dinero()  # Se asegura de guardar cambios

    def retirar_dinero_popup(self):
        """Abre una ventana emergente para ingresar la cantidad a guardar"""
        cantidad, ok = QInputDialog.getDouble(self, "Guardar Dinero", "Ingrese la cantidad a guardar:", 0.0, 0.0, self.dinero_guardado, 2)

        if ok and cantidad > 0:
            self.dinero_caja += cantidad
            self.dinero_guardado -= cantidad

            self.label_caja_dinero.setText(f"${self.dinero_caja:.2f}")
            self.label_guardado_dinero.setText(f"${self.dinero_guardado:.2f}")

            self.guardar_dinero()  # Se asegura de guardar cambios

        pass

    def guardar_dinero_popup(self):
        """Abre una ventana emergente para ingresar la cantidad a guardar"""
        cantidad, ok = QInputDialog.getDouble(self, "Guardar Dinero", "Ingrese la cantidad a guardar:", 0.0, 0.0, self.dinero_caja, 2)
        
        if ok and cantidad > 0:
            self.dinero_caja -= cantidad
            self.dinero_guardado += cantidad

            self.label_caja_dinero.setText(f"${self.dinero_caja:.2f}")
            self.label_guardado_dinero.setText(f"${self.dinero_guardado:.2f}")

            self.guardar_dinero()  # Se asegura de guardar cambios

    def guardar_dinero(self):
        """Guarda los valores de dinero en un archivo"""
        with open(self.archivo, "w") as f:
            f.write(f"{self.dinero_caja:.2f}\n{self.dinero_guardado:.2f}")

    def cargar_dinero(self):
        """Carga los valores de dinero desde un archivo"""
        try:
            with open(self.archivo, "r") as f:
                valores = f.readlines()
                return float(valores[0]), float(valores[1])
        except (FileNotFoundError, IndexError, ValueError):
            return 0.0, 0.0  # Si hay un error, inicializa en 0
            
class VentanaPrincipal(QWidget):
    """Clase para la ventana principal del programa"""
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        if self.usuario == "admn":
            self.setWindowTitle("Menú Principal - Administrador")
        else:
            self.setWindowTitle("Menú Principal - Empleado")
        self.setStyleSheet("background-color: white; color: black;")

        # Crear la instancia de la tabla (ÚNICA INSTANCIA!!)
        self.tabla = Tabla()
        self.dinero = Dinero()

        # Crear el QStackedLayout con las diferentes pantallas para simular tabulación
        self.stack_layout = QStackedLayout()
        self.pantalla_inventario = Inventario(self.tabla, usuario)
        self.pantalla_codigo = InputCodigo()
        self.pantalla_venta = Venta(self.tabla, self.dinero)  # Pasar la tabla a la venta
        self.stack_layout.addWidget(self.pantalla_inventario)  # Index 0 -> Inventario
        self.stack_layout.addWidget(self.pantalla_codigo)  # Index 1 -> Input Código  (CAMBIAR)
        self.stack_layout.addWidget(self.pantalla_venta)  # Index 2 -> Venta

        # Crear el contenedor para el stack
        self.stack_container = QWidget()
        self.stack_container.setLayout(self.stack_layout)

        # Crear los botones y pasar el stack_layout para controlar las vistas
        self.botones = Botones(self.stack_layout, self.dinero)
        self.botones.setMaximumWidth(260)

        # Layout principal
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(5)
        layout_principal.addWidget(self.botones)
        layout_principal.addWidget(self.stack_container)
        layout_principal.setStretchFactor(self.botones, 1)
        layout_principal.setStretchFactor(self.stack_container, 4)

        self.setLayout(layout_principal)

def main(usuario):
    ventana = VentanaPrincipal(usuario)
    ventana.show()
    return ventana

if __name__ == "__main__":
    usuario = "admn"
    app = QApplication(sys.argv)
    login = VentanaPrincipal(usuario)
    login.show()
    sys.exit(app.exec())
