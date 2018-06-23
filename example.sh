source dev/bin/activate
python -m cProfile -o temp.dat backtest.py -p 14400 -c USDT_BTC -u 4 -b 1000 -v mac -l 1
deactivate
