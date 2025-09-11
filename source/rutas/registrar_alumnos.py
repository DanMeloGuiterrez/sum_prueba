from flask import Blueprint, render_template, request, redirect, url_for, session
from source.database.database import obtener_conexion
import os

registrar_alumnos_bp = Blueprint('registrar_alumnos_bp', __name__)

@registrar_alumnos_bp.route('/registrar_alumnos', methods=['GET', 'POST'])
def registrar_alumnos():
    if request.method == 'POST':
        nombre          = request.form['nombre']
        apellido        = request.form['apellido']
        gmail           = request.form['gmail']
        contrasena      = request.form['contrasena']
        codigo          = request.form['codigo']
        facultad_id     = request.form['facultad']
        programa        = request.form['programa']
        especialidad    = request.form['especialidad']
        periodo         = request.form['periodo_academico']
        id_tipo_usuario = 2  

        # Manejo de la imagen
        imagen = request.files['imagen']
        nombre_imagen = "default.png"
        if imagen and imagen.filename != "":
            nombre_imagen = imagen.filename
            ruta = os.path.join("static/img", nombre_imagen)
            imagen.save(ruta)

        # Conexión a la base de datos
        conexion = obtener_conexion()
        miCursor = conexion.cursor()

        sql = """INSERT INTO alumno (
                    nombre_alumno, apellido_alumno, imagen, email, contrasena, 
                    codigo, facultad_id, programa, especialidad, periodo_academico, id_tipo_usuario
                 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        valores = (nombre, apellido, nombre_imagen, gmail, contrasena,
                   codigo, facultad_id, programa, especialidad, periodo, id_tipo_usuario)

        miCursor.execute(sql, valores)
        conexion.commit()
        id_alumno = miCursor.lastrowid

        miCursor.close()
        conexion.close()
        
        return redirect(url_for('panel_admin_bp.panel_admin'))

    # Si es GET → cargar facultades
    conexion = obtener_conexion()
    miCursor = conexion.cursor()
    miCursor.execute("SELECT id_facultad, nombre_facultad FROM facultades")
    facultades = miCursor.fetchall()
    miCursor.close()
    conexion.close()
    
    return render_template('funciones_de_la_pagina/admin/registrar_alumnos.html', facultades=facultades,
        nombre=session.get('nombre'),
        apellido=session.get('apellido')
    )
