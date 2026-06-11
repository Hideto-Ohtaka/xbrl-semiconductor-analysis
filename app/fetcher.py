import requests
import pandas as pd

HEADERS = {"User-Agent": "hideto.oh@outlook.jp"}
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

_ticker_cache: dict = {}


def _load_tickers() -> dict:
    global _ticker_cache
    if _ticker_cache:
        return _ticker_cache
    res = requests.get(TICKERS_URL, headers=HEADERS)
    data = res.json()
    _ticker_cache = {v["ticker"]: str(v["cik_str"]).zfill(10) for v in data.values()}
    return _ticker_cache


def get_cik(ticker: str) -> str | None:
    tickers = _load_tickers()
    return tickers.get(ticker.upper())


METRICS = {
    "売上高": [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
    ],
    "純利益": ["NetIncomeLoss"],
    "営業利益": ["OperatingIncomeLoss"],
    "R&D費用": ["ResearchAndDevelopmentExpense"],
}


def get_metric(cik: str, metric_name: str) -> list[dict]:
    tags = METRICS.get(metric_name, [metric_name])
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    res = requests.get(url, headers=HEADERS)
    facts = res.json().get("facts", {}).get("us-gaap", {})

    for tag in tags:
        raw = facts.get(tag, {}).get("units", {}).get("USD", [])
        if not raw:
            continue
        df = pd.DataFrame(raw)
        df = df[df["form"] == "10-K"].copy()
        df["year"] = pd.to_datetime(df["end"]).dt.year
        df = df.drop_duplicates(subset="year").sort_values("year")
        df["value"] = (df["val"] / 1e8).round(1)
        return df[["year", "value"]].to_dict(orient="records")

    return []


def get_company_name(cik: str) -> str:
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("name", cik)
