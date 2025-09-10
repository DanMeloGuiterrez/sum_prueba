from flask import Blueprint, url_for, redirect, flash, session

# Define el blueprint
cerrar_sesion_bp = Blueprint('cerrar_sesion_bp', __name__)

# Ruta del blueprint
@cerrar_sesion_bp.route('/cerrar_sesion', methods=['GET', 'POST'])
def cerrar_sesion():
    session.clear()  # Elimina toda la sesión
    flash("Sesión cerrada exitosamente.", "info")
    return redirect(url_for('inicio_de_seccion_bp.inicio_de_seccion'))
