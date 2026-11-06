"""Rutas del servicio Flask. Integración completa."""
from flask import Flask, jsonify, render_template, request, send_file
from app.db import ping_db, obtener_estadisticas, obtener_ultimas_solicitudes
from app.grafico import generar_grafico_png
from app.orchestrator import procesar_solicitud

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        try:
            db_status = ping_db()
            return jsonify(servicio="citypilot", estado="ok", db="ok" if db_status else "error")
        except Exception:
            return jsonify(servicio="citypilot", estado="degradado", db="error"), 503

    @app.post("/planificar")
    def planificar_html():
        datos = {
            "ciudad": request.form.get("ciudad"),
            "tipo": request.form.get("tipo"),
            "duracion": request.form.get("duracion"),
            "preferencias": request.form.get("preferencias", "")
        }
        
        resultado, error = procesar_solicitud(datos)
        
        if error:
            return render_template('index.html', error=error), 400
            
        return render_template('resultado.html', resultado=resultado)

    @app.post("/api/planificar")
    def planificar_api():
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se proporcionó JSON"}), 400
            
        resultado, error = procesar_solicitud(datos)
        
        if error:
            codigo_http = 400 if "validación" in error.lower() else 502
            return jsonify({"error": error}), codigo_http
            
        return jsonify(resultado), 200

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