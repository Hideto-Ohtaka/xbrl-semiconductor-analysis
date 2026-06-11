# 半導体3社 財務データ分析

SECのXBRL APIを使って、NVIDIA・AMD・Intelの売上高データを取得・可視化するJupyter Notebookです。

## 概要

- **データソース**: [SEC EDGAR XBRL API](https://www.sec.gov/edgar/sec-api-documentation)
- **対象企業**: NVIDIA (NVDA)、AMD (AMD)、Intel (INTC)
- **取得データ**: 年次売上高（10-Kファイルベース）

## セットアップ

### 1. 仮想環境の作成（推奨）

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. 必要なライブラリのインストール

```bash
pip install pandas requests matplotlib jupyter
```

### 3. Notebookを起動

```bash
jupyter notebook semiconductor_revenue_analysis.ipynb
```

セルを上から順番に実行してください。インターネット接続が必要です（SEC APIにアクセスします）。

## ファイル構成

| ファイル | 説明 |
|---|---|
| `semiconductor_revenue_analysis.ipynb` | メインのJupyter Notebook |
| `半導体3社_売上高.csv` | 取得した売上高データ（出力） |
| `NVIDIA_財務データ.csv` | NVIDIAの財務データ（出力） |

## 出力サンプル

各社の売上高推移をグラフで比較します（単位: 億ドル）。
