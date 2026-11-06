"""Pruebas básicas proporcionadas. Completar con 2 tests más por pareja."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from CityPilot_IA_Alumnos.web.app.main import create_app


def test_inicio_responde():
    client = create_app().test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"CityPilot" in response.data


def test_analitica_responde():
    client = create_app().test_client()
    assert client.get("/analitica").status_code == 200


# TODO(ALUMNADO): añadir al menos 2 tests nuevos. Ideas:
# - ciudad vacía produce 400 y NO consulta Open-Meteo;
# - la API devuelve un JSON con ciudad, clima, lugares e itinerario;
# - simulando lluvia, el prompt menciona adaptación a interior;
# - guardar una solicitud y verificar la fila SQL (integración).
# Usad mocks en pruebas unitarias para no consumir Overpass/Cohere.
