import pandas as pd

input_file = "ml/signals/tickers/generated_signals_v1_6_PETR4.csv"
output_file = "ml/signals/tickers/generated_signals_v1_6_PETR4_FIXED.csv"

df = pd.read_csv(input_file, header=0)

# Detectar si la primera columna es fecha
try:
    df["Date"] = pd.to_datetime(df["Price"], errors="raise")
    print("[OK] Columna Date reconstruida desde Price.")
except:
    print("[ERROR] Price no contiene fechas. Necesito ver el archivo original.")
    exit()

# Reordenar columnas con Date al inicio
cols = ["Date"] + [c for c in df.columns if c != "Date"]
df = df[cols]

df.to_csv(output_file, index=False)
print(f"[OK] Archivo reparado guardado en: {output_file}")

