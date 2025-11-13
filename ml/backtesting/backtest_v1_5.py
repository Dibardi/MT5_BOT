import argparse
import json
import csv
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime


def ensure_dirs(*paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)


def load_signals(path):
    df = pd.read_csv(path, parse_dates=['Date'], infer_datetime_format=True)
    df.columns = [c.strip() for c in df.columns]

    required = {"Date", "Ticker", "Open", "High", "Low", "Close", "Signal"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Archivo de señales inválido. Faltan columnas: {sorted(list(missing))}")

    return df.sort_values("Date").reset_index(drop=True)


def compute_backtest(df, capital=10000, commission=6.0, slippage=0.0005,
                     hold=5, mode="C", risk=0.01):

    trades = []
    equity = []

    cash = float(capital)
    pos_qty = 0.0
    pos_entry_price = None
    pos_entry_date = None
    pos_entry_idx = None

    equity.append({"Date": None, "equity": cash})

    for i, row in df.iterrows():
        date = row["Date"]
        signal = str(row["Signal"]).upper()

        open_price = float(row["Open"])
        close_price = float(row["Close"])

        # Cerrar posición por hold
        if pos_qty > 0 and (i - pos_entry_idx) >= hold:
            exit_price = open_price * (1 + slippage)
            proceeds = pos_qty * exit_price - commission
            pnl = proceeds - pos_qty * pos_entry_price

            cash += proceeds
            trades.append({
                "entry_date": pos_entry_date,
                "exit_date": date,
                "entry_price": pos_entry_price,
                "exit_price": exit_price,
                "qty": pos_qty,
                "pnl": pnl
            })

            pos_qty = 0
            pos_entry_price = None

        # Abrir posición
        if signal == "BUY" and pos_qty == 0:

            if mode == "A":   # full capital
                qty = (cash - commission) / (open_price * (1 + slippage))

            elif mode == "B":  # dividido entre 2 posiciones
                qty = ((cash - commission) / 2) / (open_price * (1 + slippage))

            else:  # mode C – risk based
                risk_amount = cash * risk
                stop_pct = 0.02
                qty = risk_amount / (open_price * stop_pct)

            qty = float(np.floor(qty))
            if qty > 0:
                entry_price = open_price * (1 + slippage)
                cost = qty * entry_price + commission

                if cost <= cash:
                    cash -= cost
                    pos_qty = qty
                    pos_entry_price = entry_price
                    pos_entry_date = date
                    pos_entry_idx = i

        # Equity diaria
        mtm = cash + pos_qty * close_price
        equity.append({"Date": date, "equity": float(mtm)})

    # Cerrar al final
    if pos_qty > 0:
        exit_price = float(df.iloc[-1]["Close"]) * (1 + slippage)
        proceeds = pos_qty * exit_price - commission
        pnl = proceeds - pos_qty * pos_entry_price

        cash += proceeds
        trades.append({
            "entry_date": pos_entry_date,
            "exit_date": df.iloc[-1]["Date"],
            "entry_price": pos_entry_price,
            "exit_price": exit_price,
            "qty": pos_qty,
            "pnl": pnl
        })

    equity_df = pd.DataFrame(equity)
    equity_df["equity"] = equity_df["equity"].ffill().astype(float)

    return trades, equity_df


def save_outputs(trades, equity_df, signals_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_dir = Path("ml/backtesting/output_v1_5")
    reports_dir = Path("Docs/Reports")
    ensure_dirs(out_dir, reports_dir)

    stem = Path(signals_path).stem

    trade_file = out_dir / f"trade_log_{stem}_{timestamp}.csv"
    equity_file = out_dir / f"equity_curve_{stem}_{timestamp}.csv"
    report_file = reports_dir / f"backtest_report_{stem}_{timestamp}.json"

    # Guardar trade log
    if trades:
        with trade_file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(trades[0].keys()))
            writer.writeheader()
            writer.writerows(trades)
    else:
        with trade_file.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["NO_TRADES_EXECUTED"])

    # Guardar equity
    equity_df.to_csv(equity_file, index=False)

    # Guardar reporte JSON
    report = {
        "signals": signals_path,
        "trade_log": str(trade_file),
        "equity_curve": str(equity_file),
        "n_trades": len(trades),
        "final_equity": float(equity_df["equity"].iloc[-1]),
        "timestamp": timestamp
    }
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return trade_file, equity_file, report_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", required=True)
    parser.add_argument("--mode", default="C")
    parser.add_argument("--hold", type=int, default=5)
    parser.add_argument("--capital", type=float, default=10000)
    parser.add_argument("--commission", type=float, default=6.0)
    parser.add_argument("--slippage", type=float, default=0.0005)
    parser.add_argument("--risk", type=float, default=0.01)
    args = parser.parse_args()

    df = load_signals(args.signals)

    trades, equity_df = compute_backtest(
        df,
        capital=args.capital,
        commission=args.commission,
        slippage=args.slippage,
        hold=args.hold,
        mode=args.mode,
        risk=args.risk
    )

    trade_file, equity_file, report_file = save_outputs(trades, equity_df, args.signals)

    print(f"[BACKTEST_v1_5] Trade log: {trade_file}")
    print(f"[BACKTEST_v1_5] Equity curve: {equity_file}")
    print(f"[BACKTEST_v1_5] Report: {report_file}")


if __name__ == "__main__":
    main()