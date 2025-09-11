from flask import Blueprint, url_for, redirect, render_template, session
from source.database.database import obtener_conexion

# Define el blueprint
panel_admin_bp = Blueprint('panel_admin_bp', __name__)

@panel_admin_bp.route('/panel_admin')
def panel_admin():
  
    if 'rol' in session and session['rol'] == 1:  
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Buscar la facultad
        cursor.execute(
            "SELECT id_facultad, nombre_facultad FROM facultades WHERE id_facultad = %s", 
            (session.get('facultad_id'),)
        )
        
        fila = cursor.fetchone()
        id_facultad = fila[0] if fila else None
        facultad = fila[1] if fila else "No definida"

        cursor.close()
        conexion.close()

        # Imagen por defecto si no existe
        imagen = session.get('imagen') if session.get('imagen') else 'default.png'

        return render_template(
            'funciones_de_la_pagina/panel_admin.html',
            nombre=session.get('nombre'),
            apellido=session.get('apellido'),
            imagen=imagen,
            codigo=session.get('codigo'),
            id_facultad=id_facultad,   
            facultad=facultad,   
            programa=session.get('programa'),
            especialidad=session.get('especialidad'),
            periodo=session.get('periodo_academico'),
            email=session.get('email')
        )
    
    return redirect(url_for('inicio_de_seccion_bp.inicio_de_seccion'))
