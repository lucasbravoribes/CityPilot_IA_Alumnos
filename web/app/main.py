from flask import Flask, render_template, request, jsonify
from app.orchestrator import procesar_solicitud
from app.db import ping_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planificar', methods=['POST'])
def planificar_web():
    datos = {
        "ciudad": request.form.get("ciudad"),
        "tipo": request.form.get("tipo"),
        "duracion": request.form.get("duracion"),
        "preferencias": request.form.get("preferencias", "")
    }
    
    resultado, error = procesar_solicitud(datos)
    
    if error:
        return render_template('index.html', error=error)
        
    return render_template('resultado.html', resultado=resultado)

@app.route('/api/planificar', methods=['POST'])
def planificar_api():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se proporcionó JSON"}), 400
        
    resultado, error = procesar_solicitud(datos)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify(resultado), 200

@app.route('/api/health')
def health():
    try:
        db_status = ping_db()
    except Exception:
        db_status = False
    return jsonify({"status": "ok", "db": db_status})