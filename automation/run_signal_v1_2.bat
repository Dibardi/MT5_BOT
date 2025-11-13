@echo off
cd C:\MT5_BOT
call .venv\Scripts\activate
python -m ml.signals.signal_generator --model v1_2 --append
