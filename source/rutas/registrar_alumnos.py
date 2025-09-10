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

        # Manejo de la imagen de perfil subida por el usuario
        imagen = request.files['imagen']
        nombre_imagen = None
        if imagen  and imagen.filename != "":
            nombre_imagen = imagen.filename
            ruta = os.path.join("static/img", nombre_imagen)
            imagen.save(ruta)

        # Conexión a la base de datos
        conexion = obtener_conexion()
        miCursor = conexion.cursor()

        sql = """INSERT INTO alumno (
                    nombre_alumno, apellido_alumno, imagen, email, contrasena, 
                    codigo, facultad_id, programa, especialidad, periodo_academico
                 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # Valores que se insertarán en la tabla
        valores = (nombre, apellido, nombre_imagen, gmail, contrasena,
                   codigo, facultad_id, programa, especialidad, periodo)
         # Ejecutamos la consulta de inserción
        miCursor.execute(sql, valores)
        conexion.commit()

        #  OBTENER EL ID DEL ALUMNO ANTES DE CERRAR
        id_alumno = miCursor.lastrowid

        miCursor.close()
        conexion.close()

        # Guardar datos del alumno en sesión pueda acceder a su panel sin volver a loguearse
        session['id_alumno']   = id_alumno
        session['nombre']      = nombre
        session['apellido']    = apellido
        session['email']       = gmail
        session['codigo']      = codigo
        session['facultad_id'] = facultad_id
        session['imagen']      = nombre_imagen 
        session['programa']    = programa       
        session['especialidad']= especialidad   
        session['periodo_academico'] = periodo    

        # Redirigir al panel del alumno
        return redirect(url_for('panel_alumno_bp.panel_alumno'))

    # Si es GET, mostrar el formulario con facultades
    # Cargamos la lista de facultades desde la BD para mostrarlas en el select
    conexion = obtener_conexion()
    miCursor = conexion.cursor()
    miCursor.execute("SELECT id_facultad, nombre_facultad FROM facultades")
    facultades = miCursor.fetchall()
    miCursor.close()
    conexion.close()
    
    # Renderizamos la plantilla HTML de registro
    return render_template('funciones_de_la_pagina/admin/registrar_alumnos.html', facultades=facultades)
