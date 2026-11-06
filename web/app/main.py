from flask import Blueprint, render_template, request, jsonify
from app.orchestrator import procesar_solicitud
from app.db import ping_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/planificar', methods=['POST'])
def planificar_web():
    # Extraer datos del formulario HTML
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

@main_bp.route('/api/planificar', methods=['POST'])
def planificar_api():
    # Extraer datos del body en JSON
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se proporcionó JSON"}), 400
        
    resultado, error = procesar_solicitud(datos)
    
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify(resultado), 200