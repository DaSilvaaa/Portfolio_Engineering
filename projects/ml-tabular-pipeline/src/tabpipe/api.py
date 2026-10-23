"""FastAPI model serving with strict input validation."""
import os

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from tabpipe.pipeline import add_bmi_band

Scaled = Field(ge=-0.5, le=0.5)


class Features(BaseModel):
    model_config = ConfigDict(extra="forbid")
    age: float = Scaled
    sex: float = Scaled
    bmi: float = Scaled
    bp: float = Scaled
    s1: float = Scaled
    s2: float = Scaled
    s3: float = Scaled
    s4: float = Scaled
    s5: float = Scaled
    s6: float = Scaled


class Batch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    instances: list[Features] = Field(min_length=1, max_length=100)


def create_app(model) -> FastAPI:
    app = FastAPI(title="tabpipe-api", docs_url=None, redoc_url=None)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/predict")
    def predict(body: Batch):
        df = add_bmi_band(pd.DataFrame([i.model_dump() for i in body.instances]))
        return {"predictions": [float(p) for p in model.predict(df)]}

    return app


def load_app() -> FastAPI:
    return create_app(joblib.load(os.environ.get("MODEL_PATH", "reports/model.joblib")))
