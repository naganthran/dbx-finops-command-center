import pandas as pd

def money(value):
    try:
        if pd.isna(value):
            return "$0"
        return f"${float(value):,.0f}"
    except Exception:
        return "$0"

def number(value):
    try:
        if pd.isna(value):
            return "0"
        return f"{float(value):,.0f}"
    except Exception:
        return "0"
