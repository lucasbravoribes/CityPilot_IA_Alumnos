import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import main
from app.grafico import generar_grafico_png


def test_grafico_devuelve_png_con_datos_y_sin_datos():
    stats = {"por_ciudad": [{"ciudad": "Valencia", "total": 3}],
             "por_tipo": [{"tipo_turismo": "cultural", "total": 3}]}
    for datos in (stats, {"por_ciudad": [], "por_tipo": []}):
        assert generar_grafico_png(datos).read(8) == b"\x89PNG\r\n\x1a\n"


def test_panel_y_api_degradan_con_mensaje_si_falla_la_bd(monkeypatch):
    def romper():
        raise RuntimeError("detalle interno que no debe verse")
    monkeypatch.setattr(main, "obtener_estadisticas", romper)
    client = main.create_app().test_client()
    r = client.get("/analitica")
    assert r.status_code == 200 and b"No se pudo consultar la base de datos" in r.data
    assert b"detalle interno" not in r.data and b"Traceback" not in r.data
    r = client.get("/api/estadisticas")
    assert r.status_code == 503 and b"detalle interno" not in r.data