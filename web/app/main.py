"""Rutas del servicio Flask. Integración completa."""
from flask import Flask, jsonify, render_template, request
from app.db import ping_db
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
        return render_template("analitica.html", totales=None, top_ciudades=[], ultimas=[])

    @app.get("/analitica/grafico.png")
    def grafico():
        return "Pendiente: gráfica de peticiones", 501

    @app.get("/api/estadisticas")
    def estadisticas_api():
        return jsonify(error="Pendiente: estadísticas"), 501

    return app


app = create_app()