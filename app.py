from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from source.database.database import obtener_conexion

from source.rutas.inicio_de_seccion import inicio_de_seccion_bp
from source.rutas.registrar_alumnos import registrar_alumnos_bp
from source.rutas.panel_alumno import panel_alumno_bp
from source.rutas.panel_admin import panel_admin_bp
from source.rutas.visualizar_alumnos import visualizar_alumnos_bp
from source.rutas.cerrar_sesion import cerrar_sesion_bp


app = Flask(__name__)
app.secret_key = 'secret_key'

# --- Configuracion de Gemini API ---
genai.configure(api_key="AIzaSyBpS7xVkdvlQStwzerC0yjC4yY5UR02S5I")
model = genai.GenerativeModel("gemini-2.0-flash")


app.register_blueprint(inicio_de_seccion_bp)
app.register_blueprint(registrar_alumnos_bp)
app.register_blueprint(panel_alumno_bp)
app.register_blueprint(panel_admin_bp)
app.register_blueprint(visualizar_alumnos_bp)
app.register_blueprint(cerrar_sesion_bp)


# --- Rutas principales ---
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


# --- CHATBOT ---
@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["msg"]
    response_text = get_chat_response(user_message)
    return jsonify({"response": response_text})


def get_chat_response(text):
    try:
        conexion_base_datos = obtener_conexion()
        cursor = conexion_base_datos.cursor(dictionary=True)  # -- Realiza consultas
        text_lower = text.lower()

        # --- Buscar coincidencia directa o parecida en FAQ ---
        cursor.execute("""
            SELECT respuesta FROM faq 
            WHERE SOUNDEX(pregunta) = SOUNDEX(%s) 
            OR pregunta LIKE %s
        """, (text_lower, "%" + text_lower + "%"))
        fila = cursor.fetchone()

        # --- Buscar por sinónimo si no hay coincidencia ---
        if not fila:
            cursor.execute("SELECT palabra_base, sinonimo FROM sinonimos")
            sinonimos = cursor.fetchall()
            for i in sinonimos:
                if i["sinonimo"].lower() in text_lower:
                    cursor.execute("SELECT respuesta FROM faq WHERE pregunta LIKE %s", (f"%{i['palabra_base']}%",))
                    fila = cursor.fetchone()
                    if fila:
                        break

        # --- Si hay respuesta en FAQ, devolverla ---
        if fila:
            respuesta = fila["respuesta"]
            conexion_base_datos.close()
            return respuesta

        # --- Si no hay en FAQ, Gemini una posible consulta SQL ---
        schema = """
        Tablas disponibles:
        - facultades(id_facultad INT, nombre_facultad VARCHAR(100))
        - tipo_usuario(id_tipo_usuario INT, tipo_usuario VARCHAR(100))
        - alumno(
            id_alumno INT,
            nombre_alumno VARCHAR(100),
            apellido_alumno VARCHAR(100),
            email VARCHAR(100),
            codigo INT,
            facultad_id INT,
            programa VARCHAR(100),
            especialidad VARCHAR(100),
            periodo_academico INT,
            id_tipo_usuario INT
        )
        """

        prompt_sql = f"""
        Eres un generador de consultas SQL para MySQL.
        Basado en este esquema:
        {schema}

        Genera una consulta SELECT que responda lo siguiente:
        "{text}"

        Ejemplos:
        - ¿Cuántos alumnos hay? → SELECT COUNT(*) AS total FROM alumno WHERE id_tipo_usuario = 2;
        - Muéstrame las facultades → SELECT nombre_facultad FROM facultades;
        - Qué tipos de usuario existen → SELECT tipo_usuario FROM tipo_usuario;

        Si la pregunta no requiere base de datos, responde con "NO_SQL".
        Devuelve SOLO la consulta SQL o NO_SQL.
        """

        sql_response = model.generate_content(prompt_sql)
        sql_query = sql_response.text.strip().split("\n")[0]
        print(f"[DEBUG] SQL generado: {sql_query}")

        # --- Si no requiere base de datos ---
        if "NO_SQL" in sql_query.upper():
            conexion_base_datos.close()
            prompt = f"""
            Eres un asistente del Sistema Único de Matrícula (SUM).
            Responde en español de forma breve, amable y profesional.
            El usuario preguntó: "{text}"
            """
            response = model.generate_content(prompt)
            return response.text.strip()

        # --- Validar seguridad ---
        sql_lower = sql_query.lower()
        if not sql_lower.startswith("select") or any(x in sql_lower for x in ["insert", "update", "delete", "drop", "alter"]):
            conexion_base_datos.close()
            return "Por protocolo de seguridad, solo puedo realizar consultas de lectura."

        # --- Ejecutar consulta SQL ---
        try:
            cursor.execute(sql_query)
            resultados = cursor.fetchall()
        except Exception as sql_error:
            conexion_base_datos.close()
            print("Error SQL:", sql_error)
            return f"Ocurrió un error al ejecutar la consulta SQL generada: {sql_error}"

        conexion_base_datos.close()

        # --- Formatear resultados antes de pasarlos a Gemini ---
        if len(resultados) == 0:
            data_str = "Sin resultados."
        elif len(resultados) == 1:
            data_str = str(resultados[0])
        else:
            data_str = ", ".join(str(r) for r in resultados[:10])

        # --- Interpretar resultados con Gemini ---
        prompt_final = f"""
        El usuario preguntó: "{text}"
        El resultado SQL fue: {data_str}
        Explica brevemente la respuesta en español, de manera clara, amable y natural.
        """

        final_response = model.generate_content(prompt_final)
        return final_response.text.strip()

    except Exception as e:
        print("Error general:", e)
        return "Ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo."


# --- Ejecución principal ---
if __name__ == "__main__":
    app.run(debug=True)
