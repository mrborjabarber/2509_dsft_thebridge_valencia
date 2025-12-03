# API de Productos con Flask y SQLite
# Clase de Data Science: Creacion de APIs paso a paso
# Documentacion oficial: https://flask.palletsprojects.com/

from flask import Flask, jsonify, request, g
import sqlite3

app = Flask(__name__)

# Configuracion de la base de datos
DATABASE = 'productos.db'

# Funcion para obtener conexion a la base de datos
# g es un objeto global de Flask que almacena datos durante una peticion
def get_db():
    if 'db' not in g:
        # Conectamos a la base de datos SQLite
        g.db = sqlite3.connect(DATABASE)
        # Row permite acceder a las columnas por nombre
        g.db.row_factory = sqlite3.Row
    return g.db

# Cerrar conexion al finalizar cada peticion
# Este decorador se ejecuta al terminar el contexto de la aplicacion
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Inicializar la base de datos
# Crea las tablas si no existen e inserta datos de ejemplo
def init_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Crear tabla de productos si no existe
    # INTEGER PRIMARY KEY AUTOINCREMENT: genera IDs automaticamente
    # NOT NULL: campo obligatorio
    # REAL: numero decimal para precios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')

    # Insertar datos de ejemplo si la tabla esta vacia
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ('Laptop', 1200, 'Laptop de alta gama', 10),
            ('Mouse', 25, 'Mouse inalambrico', 50),
            ('Teclado', 75, 'Teclado mecanico RGB', 30)
        ]
        # executemany ejecuta la misma consulta con diferentes valores
        cursor.executemany(
            'INSERT INTO productos (nombre, precio, descripcion, stock) VALUES (?, ?, ?, ?)',
            productos_iniciales
        )

    # commit guarda los cambios en la base de datos
    db.commit()
    db.close()

# Ruta principal - Muestra informacion de la API
@app.route('/')
def inicio():
    return jsonify({
        'mensaje': 'API de Productos con SQLite',
        'version': '1.0',
        'endpoints': {
            'GET /api/productos': 'Obtener todos los productos',
            'GET /api/productos/<id>': 'Obtener un producto especifico',
            'POST /api/productos': 'Crear un nuevo producto',
            'PUT /api/productos/<id>': 'Actualizar un producto',
            'DELETE /api/productos/<id>': 'Eliminar un producto'
        }
    })

# GET: Obtener todos los productos
# Por defecto @app.route acepta peticiones GET
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    # Obtenemos la conexion a la base de datos
    db = get_db()
    cursor = db.cursor()

    # Ejecutamos una consulta SELECT para obtener todos los productos
    cursor.execute('SELECT * FROM productos')

    # fetchall devuelve todas las filas como una lista
    filas = cursor.fetchall()

    # Convertimos cada fila a un diccionario
    # dict(fila) convierte un Row object a diccionario
    productos = [dict(fila) for fila in filas]

    # jsonify convierte datos de Python a formato JSON
    return jsonify(productos)

# GET: Obtener un producto por ID
# <int:id> captura un numero de la URL y lo pasa como parametro
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    db = get_db()
    cursor = db.cursor()

    # Usamos ? como placeholder para evitar SQL injection
    # Los valores se pasan como tupla en el segundo parametro
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))

    # fetchone devuelve solo una fila, o None si no hay resultados
    fila = cursor.fetchone()

    if fila:
        return jsonify(dict(fila))
    # 404 = Not Found
    return jsonify({'error': 'Producto no encontrado'}), 404

# POST: Crear un nuevo producto
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    # request.get_json obtiene los datos JSON del cuerpo de la peticion
    nuevo_producto = request.get_json()

    # Validacion de campos requeridos
    if not nuevo_producto or 'nombre' not in nuevo_producto or 'precio' not in nuevo_producto:
        # 400 = Bad Request (peticion mal formada)
        return jsonify({'error': 'Faltan datos requeridos: nombre y precio'}), 400

    db = get_db()
    cursor = db.cursor()

    # Insertamos el nuevo producto
    # get() devuelve el valor si existe, o un valor por defecto si no
    cursor.execute(
        'INSERT INTO productos (nombre, precio, descripcion, stock) VALUES (?, ?, ?, ?)',
        (
            nuevo_producto['nombre'],
            nuevo_producto['precio'],
            nuevo_producto.get('descripcion', ''),  # cadena vacia si no se envia
            nuevo_producto.get('stock', 0)  # 0 si no se envia
        )
    )

    # Guardamos los cambios
    db.commit()

    # lastrowid contiene el ID del registro recien insertado
    nuevo_id = cursor.lastrowid

    # Consultamos el producto creado para devolverlo completo
    cursor.execute('SELECT * FROM productos WHERE id = ?', (nuevo_id,))
    producto_creado = dict(cursor.fetchone())

    # 201 = Created (recurso creado exitosamente)
    return jsonify(producto_creado), 201

# PUT: Actualizar un producto existente
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    # Obtenemos los nuevos datos
    datos_actualizados = request.get_json()

    db = get_db()
    cursor = db.cursor()

    # Verificamos que el producto existe
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto_actual = cursor.fetchone()

    if not producto_actual:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Convertimos a diccionario para facilitar el acceso
    producto_dict = dict(producto_actual)

    # Actualizamos solo los campos que se enviaron
    # Si no se envio un campo, mantenemos el valor actual
    nuevo_nombre = datos_actualizados.get('nombre', producto_dict['nombre'])
    nuevo_precio = datos_actualizados.get('precio', producto_dict['precio'])
    nueva_descripcion = datos_actualizados.get('descripcion', producto_dict['descripcion'])
    nuevo_stock = datos_actualizados.get('stock', producto_dict['stock'])

    # Ejecutamos el UPDATE
    cursor.execute(
        'UPDATE productos SET nombre = ?, precio = ?, descripcion = ?, stock = ? WHERE id = ?',
        (nuevo_nombre, nuevo_precio, nueva_descripcion, nuevo_stock, id)
    )

    # Guardamos los cambios
    db.commit()

    # Consultamos el producto actualizado para devolverlo
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto_actualizado = dict(cursor.fetchone())

    # 200 = OK (operacion exitosa)
    return jsonify(producto_actualizado), 200

# DELETE: Eliminar un producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    db = get_db()
    cursor = db.cursor()

    # Verificamos que el producto existe antes de eliminarlo
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()

    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Eliminamos el producto
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))

    # Guardamos los cambios
    db.commit()

    # 204 = No Content (eliminacion exitosa sin cuerpo de respuesta)
    return '', 204

# Punto de entrada de la aplicacion
# Solo se ejecuta si corremos este archivo directamente
if __name__ == '__main__':
    # Inicializamos la base de datos antes de ejecutar la app
    init_db()
    print('=' * 50)
    print('Base de datos inicializada correctamente')
    print('Servidor corriendo en http://localhost:5000')
    print('=' * 50)
    print('\nEndpoints disponibles:')
    print('  GET    http://localhost:5000/api/productos')
    print('  GET    http://localhost:5000/api/productos/<id>')
    print('  POST   http://localhost:5000/api/productos')
    print('  PUT    http://localhost:5000/api/productos/<id>')
    print('  DELETE http://localhost:5000/api/productos/<id>')
    print('=' * 50)

    # debug=True permite ver errores detallados y reiniciar automaticamente
    # host='0.0.0.0' permite conexiones desde cualquier IP
    # port=5000 define el puerto donde corre el servidor
    # IMPORTANTE: En produccion, debug debe ser False por seguridad
    app.run(debug=True, host='0.0.0.0', port=5000)
