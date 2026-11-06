"""Rutas del servicio Flask. Esqueleto intencionalmente incompleto."""
from flask import Flask, jsonify, render_template, send_file
from .db import ping_db, obtener_estadisticas, obtener_ultimas_solicitudes
from .grafico import generar_grafico_png


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
        # Todo viene de PostgreSQL; si la BD falla se avisa sin mostrar traceback.
        try:
            stats = obtener_estadisticas()
            ultimas = obtener_ultimas_solicitudes(8)
        except Exception:
            return render_template("analitica.html", totales=None, top_ciudades=[], por_tipo=[],
                                   ultimas=[], error="No se pudo consultar la base de datos.")
        return render_template("analitica.html", totales=stats, top_ciudades=stats["por_ciudad"],
                               por_tipo=stats["por_tipo"], ultimas=ultimas, error=None)

    @app.get("/analitica/grafico.png")
    def grafico():
        try:
            png = generar_grafico_png(obtener_estadisticas())
        except Exception:
            return "No se pudo generar la gráfica.", 503
        # max_age=0 + no-store: el navegador no cachea y la gráfica refleja la última consulta.
        respuesta = send_file(png, mimetype="image/png", max_age=0)
        respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @app.get("/api/estadisticas")
    def estadisticas_api():
        try:
            return jsonify(obtener_estadisticas())
        except Exception:
            return jsonify(error="No se pudo consultar la base de datos."), 503

    return app


app = create_app()
