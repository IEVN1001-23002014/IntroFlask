from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@maestros_bp.route('/', methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
                    SELECT idmaestro, nombre, apaterno, amaterno, correo
                    From maestros
                """)
        
        datos = cursor.fetchall()
        maestros = [
            fila_a_diccionario(cursor,fila)
            for fila in datos
         ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'exito': False  
        }), 500
    finally:
        if cursor is not None:
            cursor.close()
@maestros_bp.route('/<idmaestro>', methods=['GET'])
def obtener_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT idmaestro, nombre, apaterno, amaterno, correo
            FROM maestros
            WHERE matricula = %s
        """
        cursor.execute(sql, (idmaestro,))
        
        # Usamos fetchone() porque solo buscamos un registro
        datos = cursor.fetchone() 

        if datos:
            maestro = fila_a_diccionario(cursor, datos)
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Mestro encontrado',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()
# POST: agregar un nuevo maestro
@maestros_bp.route('', methods=['POST'])
def agregar_maestro():
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        # Ajusta las columnas según tu base de datos
        sql = """INSERT INTO maestros (idmaestro, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        valores = (datos['id_maestro'], datos['nombre'], datos['apaterno'], datos['amaterno'], datos['correo'])
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro agregado correctamente',
            'exito': True
        }), 201

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# PUT: actualizar un maestro existente usando su ID en la URL
@maestros_bp.route('/<idmaestro>', methods=['PUT'])
def actualizar_maestro(idmaestro):
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        sql = """UPDATE maestros 
                 SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s 
                 WHERE id_maestro=%s"""
        valores = (datos['nombre'], datos['apaterno'], datos['amaterno'], datos['correo'], idmaestro)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Maestro no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Maestro actualizado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# DELETE: eliminar un maestro usando su ID en la URL
@maestros_bp.route('/<idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM maestros WHERE id_maestro=%s"
        cursor.execute(sql, (idmaestro,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Maestro no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Maestro eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()