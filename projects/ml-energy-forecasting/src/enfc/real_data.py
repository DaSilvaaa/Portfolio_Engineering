"""Dados meteorológicos reais (Open-Meteo, sem chave) e estimativa de produção fotovoltaica.

A produção NÃO é medida: é estimada com um modelo físico simplificado (estilo PVWatts) a partir da
irradiância real. Serve para treinar/avaliar o pipeline com meteorologia verdadeira.
"""
import json
import urllib.parse
import urllib.request
from datetime import date

import pandas as pd

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
LOCATIONS = {
    "Aveiro": (40.64, -8.65),
    "Lisboa": (38.72, -9.14),
    "Porto": (41.15, -8.61),
    "Faro": (37.02, -7.93),
}


def pv_from_weather(ghi_wm2: pd.Series, temp_c: pd.Series, kwp: float = 5.0, perf_ratio: float = 0.85) -> pd.Series:
    """Potência AC estimada (kW): irradiância/1000 × kWp × perda por temperatura × rácio de desempenho."""
    cell_temp = temp_c + 0.03 * ghi_wm2
    derate = (1 - 0.004 * (cell_temp - 25)).clip(lower=0.0)
    return (kwp * ghi_wm2.clip(lower=0) / 1000.0 * derate * perf_ratio).clip(lower=0.0)


def frame_from_hourly(hourly: dict, kwp: float = 5.0) -> pd.DataFrame:
    idx = pd.to_datetime(hourly["time"])
    ghi = pd.Series(hourly["shortwave_radiation"], index=idx, dtype="float64")
    temp = pd.Series(hourly["temperature_2m"], index=idx, dtype="float64")
    cloud = pd.Series(hourly["cloud_cover"], index=idx, dtype="float64") / 100.0
    df = pd.DataFrame({"pv_kw": pv_from_weather(ghi, temp, kwp), "cloud_forecast": cloud, "temp_c": temp})
    df = df.interpolate(limit=3).dropna()
    df.index.freq = pd.infer_freq(df.index)
    return df


def fetch_open_meteo(lat: float, lon: float, start: date, end: date, kwp: float = 5.0) -> pd.DataFrame:
    params = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon, "start_date": start.isoformat(), "end_date": end.isoformat(),
        "hourly": "shortwave_radiation,temperature_2m,cloud_cover", "timezone": "UTC",
    })
    req = urllib.request.Request(f"{ARCHIVE_URL}?{params}", headers={"User-Agent": "enfc/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (URL fixo https)
        payload = json.load(resp)
    return frame_from_hourly(payload["hourly"], kwp)
