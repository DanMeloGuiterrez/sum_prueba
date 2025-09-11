from flask import Blueprint, render_template, session, redirect, url_for
from source.database.database import obtener_conexion 

visualizar_alumnos_bp = Blueprint('visualizar_alumnos_bp', __name__)

@visualizar_alumnos_bp.route('/visualizar_alumnos')
def visualizar_alumnos():
    if 'rol' not in session or session['rol'] != 1:
        return redirect(url_for('inicio_de_seccion_bp.inicio_de_seccion'))  

    conexion = obtener_conexion()
    miCursor = conexion.cursor(dictionary=True)  

    sql = """
        SELECT a.id_alumno, a.nombre_alumno, a.apellido_alumno, a.imagen, 
               a.email, a.codigo, f.nombre_facultad, 
               a.programa, a.especialidad, a.periodo_academico, a.id_tipo_usuario
        FROM alumno a
        JOIN facultades f ON a.facultad_id = f.id_facultad
    """
    miCursor.execute(sql)
    usuarios = miCursor.fetchall()

    miCursor.close()
    conexion.close()
    return render_template(
        'funciones_de_la_pagina/admin/visualizar_alumnos.html',
        alumnos=usuarios,
        nombre=session.get('nombre'),
        apellido=session.get('apellido')
    )
