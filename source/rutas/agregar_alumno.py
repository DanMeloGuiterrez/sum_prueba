from flask import Blueprint, render_template

agregar_alumno_bp = Blueprint('agregar_alumno_bp', __name__)

@agregar_alumno_bp.route('/agregar_alumno')
def agregar_alumno():
    return render_template('funciones_de_la_pagina/admin/agregar_alumno.html')
