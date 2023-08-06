

<br />

<div align="center">
   <img style="margin: 0 auto; padding-bottom: 15px; padding-top: 30px" width=70%" src="https://firebasestorage.googleapis.com/v0/b/blankly-6ada5.appspot.com/o/blankly-github-logo.png?alt=media&token=8f436cd2-3d28-432c-867a-afef780f4260">
</div>
<br />

<div align="center">
  <b>💨  Rapidly build and deploy quantitative models for stocks, crypto, and forex  🚀</b>
</div>
<br />


<p align="center">
   <a target="_blank" href="https://sonarcloud.io/dashboard?id=Blankly-Finance_Blankly"><img src="https://sonarcloud.io/api/project_badges/measure?project=Blankly-Finance_Blankly&metric=sqale_rating"></a>
   <a target="_blank" href="https://sonarcloud.io/dashboard?id=Blankly-Finance_Blankly"><img src="https://sonarcloud.io/api/project_badges/measure?project=Blankly-Finance_Blankly&metric=alert_status"></a>
   <a target="_blank" href="https://github.com/Blankly-Finance/Blankly/actions/workflows/test.yml"><img src="https://github.com/Blankly-Finance/Blankly/actions/workflows/test.yml/badge.svg?branch=main"></a> <br>
   <a target="_blank" href="https://pepy.tech/project/blankly"><img src="https://pepy.tech/badge/blankly/month"></a>
   <a target="_blank" href="https://github.com/Blankly-Finance/Blankly/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/blankly?color=gree"></a>
   <a target="_blank" href="https://github.com/Blankly-Finance/Blankly/stargazers"><img src="https://img.shields.io/github/stars/blankly-finance/blankly?style=social"></a>
   <a target="_blank" href="https://discord.gg/XWcmy7Y9bb"><img src="https://img.shields.io/discord/821563936297451530.svg?color=7289da&label=Blankly%20Discord&logo=discord&style=flat"></a>
   <a target="_blank" href="https://reddit.com/r/blankly"><img src="https://badgen.net/reddit/subscribers/r/blankly"></a>
</p>
<p align="center">
    <a target="_blank" href="https://docs.blankly.finance">View Docs</a>
    ·
    <a target="_blank" href="https://blankly.finance">Our Website</a>
    ·
    <a target="_blank" href="https://blankly.substack.com">Join Our Newsletter</a>
    ·
    <a href="#quickstart">Getting Started</a>
  </p>

---

## Why Blankly? 

Blankly is an ecosystem for algotraders enabling anyone to build, monetize and scale their trading algorithms for stocks, crypto, futures or forex. The same code can be backtested, paper traded, sandbox tested and run live by simply changing a single line. Develop locally then deploy, iterate and share using the blankly platform.

Add simulated latency, social media & websocket backtests to existing models or build a new one using live data natively. Getting started is easy - just `pip install blankly` and `blankly init`.

Check out our [website](https://blankly.finance) and our [docs](https://docs.blankly.finance).

[YouTube - Under 25 Lines Build an Alpaca RSI Trading Bot](https://youtu.be/pcm0h63rhUU)
<a target="_blank" href="https://youtu.be/pcm0h63rhUU"><img src="https://firebasestorage.googleapis.com/v0/b/blankly-6ada5.appspot.com/o/github%2Fbuild_a_bot_readme_thumbnail.jpg?alt=media&token=a9dd030a-805c-447f-a970-2bc8e1815662" style="border-radius:10px"></a>

### Trade Stocks, Crypto, Futures, and Forex

```python
from blankly import Alpaca, CoinbasePro

stocks = Alpaca()
crypto = CoinbasePro()
futures = BinanceFutures()

# Easily perform the same actions across exchanges & asset types
stocks.interface.market_order('AAPL', 'buy', 1)
crypto.interface.market_order('BTC-USD', 'buy', 1)
# Full futures featureset
futures.interface.get_hedge_mode()
```

### Backtest your trades, events, websockets, and custom data

```python
import blankly
"""
This example shows how backtest over tweets
"""

class TwitterBot(blankly.Model):
    def main(self, args):
        while self.has_data:
            self.backtester.value_account()
            self.sleep('1h')

    def event(self, type_: str, data: str):
        # Now check if it's a tweet about Tesla
        if 'tsla' in data.lower() or 'gme' in data.lower():
            # Buy, sell or evaluate your portfolio
            pass


if __name__ == "__main__":
    exchange = blankly.Alpaca()
    model = TwitterBot(exchange)

    # Add the tweets json here
    model.backtester.add_custom_events(blankly.data.JsonEventReader('./tweets.json'))
    # Now add some underlying prices at 1 month
    model.backtester.add_prices('TSLA', '1h', start_date='3/20/22', stop_date='4/15/22')

    # Backtest or run live
    print(model.backtest(args=None, initial_values={'USD': 10000}))

```

**Check out alternative data examples [here](https://docs.blankly.finance/examples/model-framework)**

#### Accurate Backtest Holdings

<div align="center">
    <a><img src="https://firebasestorage.googleapis.com/v0/b/blankly-6ada5.appspot.com/o/github%2FScreen%20Shot%202022-04-17%20at%202.37.58%20PM.png?alt=media&token=d5738617-e197-4da2-850d-8fbbfda05275" style="border-radius:10px"></a>
</div>

Check out the demo link [here](https://app.blankly.finance/RETIe0J8EPSQz7wizoJX0OAFb8y1/62iIMVRKV7zkcpJysYlP/75a0c190-4d8a-44e2-9310-c47d4d72b070/backtest).

#### Iterate & Train using your Metrics, Trades and Performance

```bash
Blankly Metrics: 
Compound Annual Growth Rate (%):   54.0%
Cumulative Returns (%):            136.0%
Max Drawdown (%):                  60.0%
Variance (%):                      26.15%
Sortino Ratio:                     0.9
Sharpe Ratio:                      0.73
Calmar Ratio:                      0.99
Volatility:                        0.05
Value-at-Risk:                     358.25
Conditional Value-at-Risk:         34.16
```
### Go Live in One Line

Seamlessly run your model live!

```python
# Just turn this
strategy.backtest(to='1y')
# Into this
strategy.start()
```

Dates, times, and scheduling adjust on the backend to make the experience instant.

## Quickstart

### Installation

1. First install Blankly using `pip`. Blankly is hosted on [PyPi](https://pypi.org/project/Blankly/).

```bash
$ pip install blankly
```

2. Next, just run:
```bash
$ blankly init
```
This will initialize your working directory.

The command will create the files `keys.json`, `settings.json`, `backtest.json`, `blankly.json` and an example script called `bot.py`.

If you don't want to use our `init` command, you can find the same files in the `examples` folder under [`settings.json`](https://github.com/Blankly-Finance/Blankly/blob/main/examples/settings.json) and [`keys_example.json`](https://github.com/Blankly-Finance/Blankly/blob/main/examples/keys_example.json)

3. From there, **insert your API keys** from your exchange into the generated `keys.json` file or take advantage of the CLI keys prompt.

More information can be found on our [docs](https://docs.blankly.finance)

### Docker

1. Pull a python docker container

```bash
$ docker pull python
```

2. Move to a directory to initialize and run

```bash
$ blankly init
```

### Directory format

The working directory format should have *at least* these files:
```
Project
   |-bot.py
   |-keys.json
   |-settings.json
```

#### Additional Info

Make sure you're using a supported version of python. The module is currently tested on these versions:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10

For more info, and ways to do more advanced things, check out our [getting started docs](https://docs.blankly.finance).

## Supported Exchanges

| Exchange            | Live Trading | Websockets | Paper Trading | Backtesting |
| ------------------- |--------------| ---------- |--------------| ----------- |
| Coinbase Pro        | 🟢           | 🟢          | 🟢           | 🟢           |
| Binance             | 🟢           | 🟢          | 🟢           | 🟢           |
| Alpaca              | 🟢           | 🟢          | 🟢           | 🟢           |
| OANDA               | 🟢           |  | 🟢           | 🟢           |
| FTX                 | 🟢           | 🟢          | 🟢           | 🟢           |
| KuCoin              | 🟢           | 🟢        | 🟢           | 🟢           |
| Binance Futures | 🟢 | 🟢 | 🟢 | 🟢 |
| FTX Futures | 🟡 | 🟡 | 🟢 | 🟢 |
| Okx | 🟢 | 🟢 | 🟢 | 🟢 |
| Kraken              | 🟡           | 🟡          | 🟡           | 🟡           |
| Keyless Backtesting |              |            |              | 🟢           |
| TD Ameritrade       | 🔴           | 🔴          | 🔴           | 🔴           |
| Webull              | 🔴           | 🔴          | 🔴           | 🔴           |
| Robinhood           | 🔴           | 🔴          | 🔴           | 🔴           |


🟢  = working

🟡  = in development, some or most features are working

🔴  = planned but not yet in development

## RSI Example

We have a pre-built cookbook examples that implement strategies such as RSI, MACD, and the Golden Cross found in our [examples](https://docs.blankly.finance/examples/golden-cross).

The model below will run an RSI check every 30 minutes - **buying** below **30** and **selling** above **70**. Try switching the exchange and assets and see how it instantly works on Binance, Coinbase Pro or anything else you trade on.

```python
import blankly
from blankly import StrategyState


def price_event(price, symbol, state: StrategyState):
    """ This function will give an updated price every 15 seconds from our definition below """
    state.variables['history'].append(price)
    rsi = blankly.indicators.rsi(state.variables['history'])
    
    if rsi[-1] < 30 and not state.variables['has_bought']:
        # Dollar cost average buy
        state.variables['has_bought'] = True
        state.interface.market_order(symbol, side='buy', size=1)
    elif rsi[-1] > 70 and state.variables['has_bought']:
        # Dollar cost average sell
        state.variables['has_bought'] = False
        state.interface.market_order(symbol, side='sell', size=1)


def init(symbol, state: StrategyState):
    # Download price data to give context to the algo
    state.variables['history'] = state.interface.history(symbol, to='1y', return_as='list')['open']
    state.variables['has_bought'] = False


if __name__ == "__main__":
    # Authenticate on alpaca to create a strategy
    alpaca = blankly.Alpaca()

    # Use our strategy helper on alpaca
    strategy = blankly.Strategy(alpaca)

    # Run the price event function every time we check for a new price - by default that is 15 seconds
    strategy.add_price_event(price_event, symbol='NCLH', resolution='30m', init=init)
    strategy.add_price_event(price_event, symbol='CRBP', resolution='1h', init=init)
    strategy.add_price_event(price_event, symbol='D', resolution='15m', init=init)
    strategy.add_price_event(price_event, symbol='GME', resolution='30m', init=init)

    # Start the strategy. This will begin each of the price event ticks
    # strategy.start()
    # Or backtest using this
    strategy.backtest(to='1y')
```
## Other Info

### Subscribe to our news!
https://blankly.substack.com/p/coming-soon

### Bugs

Please report any bugs or issues on the GitHub's Issues page.

### Disclaimer 

Trading is risky. We are not responsible for losses incurred using this software, software fitness for any particular purpose, or responsibility for any issues or bugs.
This is free software.

### Contributing

If you would like to support the project, pull requests are welcome.
You can also contribute just by telling us what you think of Blankly: https://forms.gle/4oAjG9MKRTYKX2hP9

### Licensing 

**Blankly** is distributed under the [**LGPL License**](https://www.gnu.org/licenses/lgpl-3.0.en.html). See the [LICENSE](/LICENSE) for more details.

New updates every day 💪.
