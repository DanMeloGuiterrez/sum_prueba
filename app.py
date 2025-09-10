from flask import Flask, render_template

#Funciones
from source.rutas.inicio_de_seccion import inicio_de_seccion_bp
from source.rutas.registrar_alumnos import registrar_alumnos_bp
from source.rutas.panel_alumno import panel_alumno_bp
from source.rutas.cerrar_sesion import cerrar_sesion_bp

app = Flask(__name__)
app.secret_key = 'secret_key' 

# Funciones de la Pagina
app.register_blueprint(inicio_de_seccion_bp)
app.register_blueprint(registrar_alumnos_bp)
app.register_blueprint(panel_alumno_bp) 
app.register_blueprint(cerrar_sesion_bp)

@app.route("/")
def index():
    return render_template("transicion.html")

@app.route("/portafolio")
def portafolio():
    return render_template("vistas_encabezada/portafolio.html")

@app.route("/quienes_somos")
def QuienesSomos():
    return render_template("vistas_encabezada/quienes_somos.html")

@app.route("/enlaces_internos")
def EnlacesInternos():
    return render_template("vistas_encabezada/enlaces_internos.html")

@app.route("/enlaces_externos")
def EnlacesExternos():
    return render_template("vistas_encabezada/enlaces_externos.html")

@app.route("/contacto")
def Contacto():
    return render_template("vistas_encabezada/contacto.html")

if __name__ == "__main__":
    app.run(debug=True)
