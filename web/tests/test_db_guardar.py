import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import _parametros_insert

REGISTRO = {
    "ciudad": "Valencia", "tipo_turismo": "cultural", "duracion_horas": 4,
    "meteorologia": {"temperatura_c": 20.5}, "lugares": [{"nombre": "Lonja de la Seda"}],
    "COHERE_API_KEY": "secreto-que-no-debe-guardarse",
}


def test_parametros_insert_jsonb_defaults_y_sin_claves_extra():
    p = _parametros_insert(REGISTRO)
    assert json.loads(p["meteorologia"]) == {"temperatura_c": 20.5}
    assert json.loads(p["lugares"])[0]["nombre"] == "Lonja de la Seda"
    assert p["preferencias"] == "" and p["estado"] == "ok" and p["modo_demo"] is False
    assert "COHERE_API_KEY" not in p and "secreto" not in json.dumps(p)