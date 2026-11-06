"""Rutas del servicio Flask. Esqueleto intencionalmente incompleto."""
from flask import Flask, jsonify, render_template
from CityPilot_IA_Alumnos.web.app.db import ping_db


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        # TODO(ALUMNADO): El formulario se desarrolla en templates/index.html.
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        # Punto de salud proporcionado para verificar Compose y PostgreSQL.
        try:
            ping_db()
            return jsonify(servicio="citypilot", estado="ok", db="ok")
        except Exception:
            return jsonify(servicio="citypilot", estado="degradado", db="error"), 503

    @app.post("/planificar")
    def planificar_html():
        # TODO(ALUMNADO): leer y validar request.form; llamar a UN orquestador
        # compartido con /api/planificar; renderizar resultado.html.
        return "Pendiente: formulario -> integración -> resultado", 501

    @app.post("/api/planificar")
    def planificar_api():
        # TODO(ALUMNADO): leer JSON, usar EL MISMO orquestador y devolver JSON.
        # Nunca duplicar la lógica de datos externos en las dos rutas.
        return jsonify(error="Pendiente: API propia"), 501

    @app.get("/analitica")
    def analitica():
        # TODO(ALUMNADO): consultar PostgreSQL y pasar métricas a la plantilla.
        return render_template("analitica.html", totales=None, top_ciudades=[], ultimas=[])

    @app.get("/analitica/grafico.png")
    def grafico():
        # TODO(ALUMNADO): generar una gráfica PNG de Matplotlib con datos SQL,
        # utilizando un BytesIO y Flask send_file. No JavaScript.
        return "Pendiente: gráfica de peticiones", 501

    @app.get("/api/estadisticas")
    def estadisticas_api():
        # TODO(ALUMNADO): exponer el resumen de la base de datos como JSON.
        return jsonify(error="Pendiente: estadísticas"), 501

    return app


app = create_app()
