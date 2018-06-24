CryptoTrader

|    Parameter   | Default  | Description                                                                         | Strategies |
|:--------------:|----------|-------------------------------------------------------------------------------------|------------|
| lookback       | 7        | The pattern size for matching                                                       |            |
| learnProgTotal | 1400      | The total learning that should be done before trading can start.                    |            |
| advance        | 5        | How far ahead should be looked ahead for future outcomes                            |            |
| howSimReq      | 0.95     | How similar patterns should be to be considered a match. (0-1)                      |            |
| learnLimit     | 700      | The max number of learned patterns the program should keep in memory                |            |
| highMA         | 47       | High moving average (for crossover)                                                 |            |
| lowMA          | 28       | Low moving average (for crossover)                                                  |            |
| mamultfactor   | 1        | How much the highMa and lowMa should cross by                                       |            |
| numSimulTrades | 1        | The number of simultaneous trades allowed                                           |            |
| stoploss       | 0        | Stop loss (between 0-1). Stop loss price will be calculated as price * (1-stoploss) |            |
| lowrsi         | 30       | What is considered a low RSI                                                        |            |
| highrsi        | 70       | What is considered a high RSI                                                       |            |
| rsiperiod      | 14       | The RSI period                                                                      |            |
| upfactor       | 1.1      | What is considered an upward price movement                                         |            |
| downfactor     | 1.3      | What is considered a download price movement                                        |            |
| trailingstop   | 0.1      | Trailing stop (similar to stoploss)                                                 |            |