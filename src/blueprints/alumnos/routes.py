from flask import Blueprint,jsonify,request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

# GET: consultar todos los alumnos
@alumnos_bp.route('/',methods=['GET'])
def lista_alumnos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT matricula, nombre, apaterno, amaterno, correo
            From alumnos
        """)

        datos = cursor.fetchall()
        alumnos = [
            fila_a_diccionario(cursor,fila)
            for fila in datos
        ]

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        
        }), 200

    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los alumnos',
            'exito': False  
        }), 500
    finally:
        if cursor is not None:
            cursor.close()
# GET: consultar un alumno específico por su matricula
@alumnos_bp.route('/<matricula>', methods=['GET'])
def obtener_alumno(matricula):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumnos
            WHERE matricula = %s
        """
        cursor.execute(sql, (matricula,))
        
        # Usamos fetchone() porque solo buscamos un registro
        datos = cursor.fetchone() 

        if datos:
            alumno = fila_a_diccionario(cursor, datos)
            return jsonify({
                'alumno': alumno,
                'mensaje': 'Alumno encontrado',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }), 404

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()
# POST: agregar un nuevo alumno
@alumnos_bp.route('/<matricula>', methods=['POST'])
def agregar_alumno(matricula):
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        valores = (datos['matricula'], datos['nombre'], datos['apaterno'], datos['amaterno'], datos['correo'])
        
        cursor.execute(sql, valores)
        mysql.connection.commit() # Importante para guardar los cambios

        return jsonify({
            'mensaje': 'Alumno agregado correctamente',
            'exito': True
        }), 201

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# PUT: actualizar un alumno existente usando su matricula en la URL
@alumnos_bp.route('/<matricula>', methods=['PUT'])
def actualizar_alumno(matricula):
    cursor = None
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        
        sql = """UPDATE alumnos 
                 SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s 
                 WHERE matricula=%s"""
        valores = (datos['nombre'], datos['apaterno'], datos['amaterno'], datos['correo'], matricula)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        # Verificar si realmente se actualizó algún registro
        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Alumno no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Alumno actualizado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

# DELETE: eliminar un alumno usando su matricula en la URL
@alumnos_bp.route('/<matricula>', methods=['DELETE'])
def eliminar_alumno(matricula):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM alumnos WHERE matricula=%s"
        cursor.execute(sql, (matricula,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'mensaje': 'Alumno no encontrado', 'exito': False}), 404

        return jsonify({
            'mensaje': 'Alumno eliminado correctamente',
            'exito': True
        }), 200

    except Exception as e:
        return jsonify({'mensaje': str(e), 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()