from flask import Blueprint, url_for, redirect, render_template, session
from source.database.database import obtener_conexion

# Define el blueprint
panel_alumno_bp = Blueprint('panel_alumno_bp', __name__)

# Ruta del blueprint
@panel_alumno_bp.route('/panel_alumno')
def panel_alumno():
    if session:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Busca en la tabla facultades los datos de la facultad cuyo ID está guardado en la sesión
        cursor.execute("SELECT id_facultad, nombre_facultad FROM facultades WHERE id_facultad = %s", 
                       (session.get('facultad_id'),))
        
        fila = cursor.fetchone()
        id_facultad = fila[0] if fila else None
        facultad = fila[1] if fila else "No definida"

        cursor.close()
        conexion.close()

        return render_template(
            'funciones_de_la_pagina/panel_alumno.html',
            nombre=session.get('nombre'),
            apellido=session.get('apellido'),
            imagen=session.get('imagen'),
            codigo=session.get('codigo'),
            id_facultad=id_facultad,   
            facultad=facultad,   
            programa=session.get('programa'),
            especialidad=session.get('especialidad'),
            periodo=session.get('periodo_academico'),
            email=session.get('email')
        )
    
    return render_template('funciones_de_la_pagina/panel_alumno.html')
