"""Dashboard Streamlit: previsão day-ahead de produção fotovoltaica com meteorologia real.

Executar:  streamlit run app.py   (a partir de projects/ml-energy-forecasting)
"""
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))

from enfc.model import evaluate  # noqa: E402
from enfc.real_data import LOCATIONS, fetch_open_meteo  # noqa: E402

st.set_page_config(page_title="Previsão solar day-ahead", layout="wide")
st.title("☀️ Previsão fotovoltaica day-ahead")
st.caption(
    "Meteorologia real (Open-Meteo). A produção é **estimada** por um modelo físico simplificado a partir da "
    "irradiância; o modelo de ML é comparado com baselines ingénuas num teste estritamente posterior ao treino."
)

with st.sidebar:
    place = st.selectbox("Localização", list(LOCATIONS))
    kwp = st.slider("Potência instalada (kWp)", 1.0, 50.0, 5.0, 0.5)
    years = st.slider("Histórico (anos)", 1, 3, 2)


@st.cache_data(show_spinner="A obter dados meteorológicos...", ttl=24 * 3600)
def load(place: str, kwp: float, years: int) -> pd.DataFrame:
    end = date.today() - timedelta(days=7)
    return fetch_open_meteo(*LOCATIONS[place], end - timedelta(days=365 * years), end, kwp)


@st.cache_data(show_spinner="A treinar o modelo...")
def run(place: str, kwp: float, years: int):
    res = evaluate(df=load(place, kwp, years))
    return res["metrics"], res["test"]


try:
    metrics, test = run(place, kwp, years)
except OSError as e:
    st.error(f"Não foi possível obter dados meteorológicos: {e}")
    st.stop()

m = metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("MAE do modelo", f"{m['model']['mae']:.3f} kW")
c2.metric("MAE persistência", f"{m['persistence_24h']['mae']:.3f} kW")
c3.metric("Ganho de RMSE vs persistência", f"{m['skill_vs_persistence_rmse']:.1%}")
c4.metric("Horas de teste", f"{m['n_test']}")

st.subheader("Previsão vs. valor real")
span = st.slider("Dias a mostrar", 3, 30, 7)
window = test.iloc[: span * 24][["target", "pred"]].rename(columns={"target": "Real (estimado)", "pred": "Previsão"})
st.line_chart(window)

left, right = st.columns(2)
with left:
    st.subheader("Comparação com baselines")
    st.dataframe(
        pd.DataFrame(
            {
                "MAE (kW)": [m[k]["mae"] for k in ("model", "persistence_24h", "seasonal_naive_168h")],
                "RMSE (kW)": [m[k]["rmse"] for k in ("model", "persistence_24h", "seasonal_naive_168h")],
                "MAE diurno (kW)": [m[k]["mae_daylight"] for k in ("model", "persistence_24h", "seasonal_naive_168h")],
            },
            index=["Gradient Boosting", "Persistência (t-24h)", "Sazonal ingénua (t-168h)"],
        ).round(3)
    )
with right:
    st.subheader("Erro médio por hora do dia")
    err = (test["target"] - test["pred"]).abs().groupby(test["hour"]).mean()
    st.bar_chart(err.rename("MAE (kW)"))

st.caption(
    f"Validação cruzada temporal (3 janelas expansivas): MAE {m['cv_mae_mean']:.3f} ± {m['cv_mae_std']:.3f} kW. "
    "Limitação: as variáveis meteorológicas são observadas (reanálise), não previsões históricas, o que é otimista."
)
