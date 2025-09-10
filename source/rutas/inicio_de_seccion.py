from flask import Blueprint, render_template, url_for, request, redirect, session
# - render_template: para mostrar plantillas HTML
# - url_for: para obtener URLs de rutas registradas
# - request: para acceder a los datos enviados en formularios
from source.database.database import obtener_conexion 

# Define el blueprint
inicio_de_seccion_bp = Blueprint('inicio_de_seccion_bp', __name__)

@inicio_de_seccion_bp.route('/inicio_de_seccion', methods=["POST", "GET"])
# Permite acceder con GET (para mostrar el formulario) y POST (para procesar login)
def inicio_de_seccion():
    if request.method == "POST":
        email = request.form["username"]     
        password = request.form["contrasena"]
        
        conexion = obtener_conexion()
        cursor = conexion.cursor(buffered=True)  
        cursor.execute("""
            SELECT id_alumno, nombre_alumno, apellido_alumno, imagen, email, contrasena,
                   codigo, facultad_id, programa, especialidad, periodo_academico
            FROM alumno WHERE email = %s
        """, (email,)) # Consulta al alumno que tenga el email ingresado

        fila_alumno = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if fila_alumno: 
            # fila_alumno[5] = contraseña en la BD
            if fila_alumno[5].strip() == password:  
                # Compara la contraseña ingresada (password) con la de la BD (fila_alumno[5])
                
                # Guardar datos en la sesión
                session['id_alumno'] = fila_alumno[0]
                session['nombre'] = fila_alumno[1]
                session['apellido'] = fila_alumno[2]
                session['imagen'] = fila_alumno[3]
                session['email'] = fila_alumno[4]
                session['codigo'] = fila_alumno[6]
                session['facultad_id'] = fila_alumno[7]
                session['programa'] = fila_alumno[8]
                session['especialidad'] = fila_alumno[9]
                session['periodo_academico'] = fila_alumno[10]

                # Redirigir al panel del alumno
                
                return redirect(url_for('panel_alumno_bp.panel_alumno'))
            else: # Contraseña ta mal 
                return render_template('funciones_de_la_pagina/inicio_de_seccion.html')
        else: # Alumno no contrado
            return render_template('funciones_de_la_pagina/inicio_de_seccion.html')
    
    return render_template('funciones_de_la_pagina/inicio_de_seccion.html')

