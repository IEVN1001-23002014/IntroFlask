from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

# GET: consultar todos los administrativos
@administrativos_bp.route('', methods=['GET'])
def lista_administrativos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT numempleado, nombre, apellidos, telefono, correo, departamento
            FROM administrativos
        """)
        datos = cursor.fetchall()
        
        administrativos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# GET: consultar un administrativo específico por su numempleado
@administrativos_bp.route('/<numempleado>', methods=['GET'])
def obtener_administrativo(numempleado):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT numempleado, nombre, apellidos, telefono, correo, departamento
            FROM administrativos
            WHERE numempleado = %s
        """
        cursor.execute(sql, (numempleado,))
        datos = cursor.fetchone() 

        if datos:
            administrativo = fila_a_diccionario(cursor, datos)
            return jsonify({
                'administrativo': administrativo,
                'mensaje': 'Administrativo encontrado',
                'exito': True
            }), 200
        else:
            return jsonify({'mensaje': 'Administrativo no encontrado', 'exito': False}), 404

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# POST: agregar un nuevo administrativo (Corregido: sin argumentos en la URL)
@administrativos_bp.route('', methods=['POST'])
def agregar_administrativo():
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        sql = """INSERT INTO administrativos (numempleado, nombre, apellidos, telefono, correo, departamento) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (datos['numempleado'], datos['nombre'], datos['apellidos'], datos['telefono'], datos['correo'], datos['departamento'])
        
        cursor.execute(sql, valores)
        mysql.connection.commit() 

        return jsonify({
            'mensaje': 'Administrativo agregado correctamente',
            'exito': True
        }), 201

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# PUT: actualizar un administrativo existente usando su numempleado en la URL
@administrativos_bp.route('/<numempleado>', methods=['PUT'])
def actualizar_administrativo(numempleado):
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        sql = """UPDATE administrativos 
                 SET nombre=%s, apellidos=%s, telefono=%s, correo=%s, departamento=%s 
                 WHERE numempleado=%s"""
        valores = (datos['nombre'], datos['apellidos'], datos['telefono'], datos['correo'], datos['departamento'], numempleado)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Administrativo no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Administrativo actualizado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# DELETE: eliminar un administrativo usando su numempleado en la URL
@administrativos_bp.route('/<numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM administrativos WHERE numempleado=%s"
        cursor.execute(sql, (numempleado,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Administrativo no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Administrativo eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()