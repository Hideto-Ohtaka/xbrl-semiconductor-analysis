from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.fetcher import get_cik, get_metric, get_company_name, METRICS
import os

app = FastAPI(title="企業財務分析")

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.get("/api/metrics")
def list_metrics():
    return {"metrics": list(METRICS.keys())}


@app.get("/api/company/{ticker}")
def company_info(ticker: str):
    cik = get_cik(ticker)
    if not cik:
        raise HTTPException(status_code=404, detail=f"{ticker} が見つかりません")
    name = get_company_name(cik)
    return {"ticker": ticker.upper(), "cik": cik, "name": name}


class CompareRequest(BaseModel):
    tickers: list[str]
    metric: str


@app.post("/api/compare")
def compare(req: CompareRequest):
    result = []
    for ticker in req.tickers:
        cik = get_cik(ticker)
        if not cik:
            continue
        name = get_company_name(cik)
        data = get_metric(cik, req.metric)
        result.append({"ticker": ticker.upper(), "name": name, "data": data})
    return {"metric": req.metric, "companies": result}
