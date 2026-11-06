"""Tests propios de contratos y manejo de errores de los clientes externos."""
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import api_clients


def test_geocodificar_distingue_ciudad_sin_resultados(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {"results": None}
    monkeypatch.setattr(api_clients.requests, "get", Mock(return_value=respuesta))

    with pytest.raises(api_clients.SinResultadosError):
        api_clients.geocodificar("CiudadInventada")


def test_obtener_meteorologia_normaliza_campos_actuales(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {
        "current": {
            "temperature_2m": 21.5,
            "precipitation": 0.2,
            "weather_code": 61,
            "time": "2026-11-06T08:00",
        }
    }
    peticion = Mock(return_value=respuesta)
    monkeypatch.setattr(api_clients.requests, "get", peticion)

    resultado = api_clients.obtener_meteorologia(39.47, -0.38)

    assert resultado == {
        "temperatura_c": 21.5,
        "precipitacion_mm": 0.2,
        "codigo_tiempo": 61,
        "instante": "2026-11-06T08:00",
    }
    assert peticion.call_args.kwargs["timeout"] == api_clients.HTTP_TIMEOUT
    assert peticion.call_args.kwargs["params"]["timezone"] == "auto"


def test_overpass_normaliza_nodos_y_ways_y_limita_radio(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {
        "elements": [
            {
                "type": "node",
                "lat": 39.47,
                "lon": -0.38,
                "tags": {"name": "Museo Central", "tourism": "museum"},
            },
            {
                "type": "way",
                "center": {"lat": 39.48, "lon": -0.37},
                "tags": {"name": "Galería Norte", "tourism": "gallery"},
            },
            {
                "type": "node",
                "lat": 39.47,
                "lon": -0.38,
                "tags": {"tourism": "museum"},
            },
        ]
    }
    peticion = Mock(return_value=respuesta)
    monkeypatch.setattr(api_clients.requests, "post", peticion)

    lugares = api_clients.obtener_lugares(39.47, -0.38, "cultural")

    assert len(lugares) == 2
    assert lugares[0]["fuente"] == "OpenStreetMap"
    assert lugares[0]["demo"] is False
    assert lugares[1]["lat"] == 39.48
    consulta = peticion.call_args.kwargs["data"]["data"]
    assert "around:2500,39.47,-0.38" in consulta
    assert peticion.call_args.kwargs["timeout"] == api_clients.OVERPASS_TIMEOUT


def test_error_http_de_overpass_se_propaga(monkeypatch):
    respuesta = Mock()
    respuesta.raise_for_status.side_effect = requests.HTTPError("504 Gateway Timeout")
    monkeypatch.setattr(api_clients.requests, "post", Mock(return_value=respuesta))

    with pytest.raises(requests.HTTPError):
        api_clients.obtener_lugares(39.47, -0.38, "naturaleza")


def test_tipo_invalido_no_consulta_overpass(monkeypatch):
    peticion = Mock()
    monkeypatch.setattr(api_clients.requests, "post", peticion)

    with pytest.raises(ValueError):
        api_clients.obtener_lugares(39.47, -0.38, "lo_que_quiera")

    peticion.assert_not_called()


def test_geocodificar_normaliza_respuesta_y_parametros(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {
        "results": [{
            "name": "Valencia",
            "country": "Espa?a",
            "latitude": 39.4699,
            "longitude": -0.3763,
        }]
    }
    peticion = Mock(return_value=respuesta)
    monkeypatch.setattr(api_clients.requests, "get", peticion)

    resultado = api_clients.geocodificar(" Valencia ")

    assert resultado == {
        "ciudad": "Valencia",
        "pais": "Espa?a",
        "lat": 39.4699,
        "lon": -0.3763,
    }
    assert peticion.call_args.kwargs["params"] == {
        "name": "Valencia",
        "count": 1,
        "language": "es",
        "countryCode": "ES",
    }
    assert peticion.call_args.kwargs["timeout"] == api_clients.HTTP_TIMEOUT


def test_geocodificar_propaga_error_http(monkeypatch):
    respuesta = Mock()
    respuesta.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
    monkeypatch.setattr(api_clients.requests, "get", Mock(return_value=respuesta))

    with pytest.raises(requests.HTTPError):
        api_clients.geocodificar("Valencia")


def test_coordenadas_invalidas_no_generan_peticion_meteorologica(monkeypatch):
    peticion = Mock()
    monkeypatch.setattr(api_clients.requests, "get", peticion)

    with pytest.raises(ValueError):
        api_clients.obtener_meteorologia(91, -0.38)

    peticion.assert_not_called()


def test_overpass_sin_elementos_devuelve_lista_vacia(monkeypatch):
    respuesta = Mock()
    respuesta.json.return_value = {"elements": []}
    monkeypatch.setattr(api_clients.requests, "post", Mock(return_value=respuesta))

    assert api_clients.obtener_lugares(39.47, -0.38, "cultural") == []
