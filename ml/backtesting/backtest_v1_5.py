# backtest_v1_5.py — Fix para FutureWarning

import pandas as pd
import numpy as np

# Esta es solo la parte corregida (línea del warning):
# Reemplazar donde corresponda en tu código completo:
#
#   cum = equity_df['equity'].fillna(method='ffill').astype(float).values
#
# por:

def fix_warning(equity_df):
    cum = equity_df['equity'].ffill().astype(float).values
    return cum

print("[BACKTEST_FIX] Este archivo contiene el fix aplicado correctamente.")