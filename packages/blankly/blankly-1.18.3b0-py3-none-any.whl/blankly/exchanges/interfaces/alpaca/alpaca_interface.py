"""
    alpaca API Interface Definition
    Copyright (C) 2021  Arun Annamalai, Emerson Dove, Brandon Fan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import time
import warnings
from datetime import datetime as dt, timezone

import alpaca_trade_api
import pandas as pd
from alpaca_trade_api.rest import APIError as AlpacaAPIError, TimeFrame

from blankly.exchanges.interfaces.exchange_interface import ExchangeInterface
from blankly.exchanges.orders.limit_order import LimitOrder
from blankly.exchanges.orders.market_order import MarketOrder
from blankly.exchanges.orders.stop_loss import StopLossOrder
from blankly.exchanges.orders.take_profit import TakeProfitOrder
from blankly.utils import utils as utils
from blankly.utils.exceptions import APIException
from blankly.utils.time_builder import build_minute, time_interval_to_seconds, number_interval_to_string


class AlpacaInterface(ExchangeInterface):
    def __init__(self, exchange_name, authenticated_api):
        self.__unique_assets = None
        super().__init__(exchange_name, authenticated_api, valid_resolutions=[60, 60 * 5, 60 * 15,
                                                                              60 * 60 * 24])
        assert isinstance(self.calls, alpaca_trade_api.REST)

    def init_exchange(self):
        try:
            account_info = self.calls.get_account()
        except alpaca_trade_api.rest.APIError as e:
            raise APIException(e.__str__() + ". Are you trying to use your normal exchange keys "
                                             "while in sandbox mode? \nTry toggling the \'sandbox\' setting "
                                             "in your keys.json or check if the keys were input correctly into your "
                                             "keys.json.")
        try:
            if account_info['account_blocked']:
                warnings.warn('Your alpaca account is indicated as blocked for trading....')
        except KeyError:
            raise LookupError("alpaca API call failed")

        filtered_assets = []
        products = self.calls.list_assets(status=None, asset_class=None)
        for i in products:
            if i['symbol'] not in filtered_assets and i['status'] != 'inactive':
                filtered_assets.append(i['symbol'])
            else:
                # TODO handle duplicate symbols
                pass
        self.__unique_assets = filtered_assets

    def get_products(self) -> dict:
        """
        [
            {
              "id": "904837e3-3b76-47ec-b432-046db621571b",
              "class": "us_equity",
              "exchange": "NASDAQ",
              "symbol": "AAPL",
              "status": "active",
              "tradable": true,
              "marginable": true,
              "shortable": true,
              "easy_to_borrow": true,
              "fractionable": true
            },
            ...
        ]
        """
        needed = self.needed['get_products']
        assets = self.calls.list_assets(status=None, asset_class=None)

        for asset in assets:
            base_asset = asset['symbol']
            asset['symbol'] = base_asset
            asset['base_asset'] = base_asset
            asset['quote_asset'] = 'USD'
            if asset['fractionable']:
                asset['base_min_size'] = .000000001
                asset['base_increment'] = .000000001
            else:
                asset['base_min_size'] = 1
                asset['base_increment'] = 1
            asset['base_max_size'] = 10000000000

        for i in range(len(assets)):
            assets[i] = utils.isolate_specific(needed, assets[i])

        return assets

    @property
    def cash(self):
        account_dict = self.calls.get_account()
        return float(account_dict['buying_power'])

    @utils.enforce_base_asset
    def get_account(self, symbol=None):
        assert isinstance(self.calls, alpaca_trade_api.REST)

        symbol = super().get_account(symbol)

        positions = self.calls.list_positions()
        positions_dict = utils.AttributeDict({})

        for position in positions:
            curr_symbol = position.pop('symbol')
            positions_dict[curr_symbol] = utils.AttributeDict({
                'available': float(position.pop('qty')),
                'hold': 0.0
            })

        symbols = list(positions_dict.keys())
        # Catch an edge case bug that if there are no positions it won't try to snapshot
        if len(symbols) != 0:
            open_orders = self.calls.list_orders(status='open', symbols=symbols)
            snapshot_price = self.calls.get_snapshots(symbols=symbols)
        else:
            open_orders = []
            snapshot_price = {}

        # now grab the available cash in the account
        account = self.calls.get_account()
        positions_dict['USD'] = utils.AttributeDict({
            'available': float(account['buying_power']),
            'hold': 0.0
        })

        for order in open_orders:
            curr_symbol = order['symbol']
            if order['side'] == 'buy':  # buy orders only affect USD holds
                if order['qty']:  # this case handles qty market buy and limit buy
                    if order['type'] == 'limit':
                        dollar_amt = float(order['qty']) * float(order['limit_price'])
                    elif order['type'] == 'market':
                        dollar_amt = float(order['qty']) * snapshot_price[curr_symbol]['latestTrade']['p']
                    else:  # we don't have support for stop_order, stop_limit_order
                        dollar_amt = 0.0
                else:  # this is the case for notional market buy
                    dollar_amt = float(order['notional'])

                # In this case we don't have to subtract because the buying power is the available money already
                # we just need to add to figure out how much is actually on limits
                # positions_dict['USD']['available'] -= dollar_amt

                # So just add to our hold
                positions_dict['USD']['hold'] += dollar_amt

            else:
                if order['qty']:  # this case handles qty market sell and limit sell
                    qty = float(order['qty'])
                else:  # this is the case for notional market sell, calculate the qty with cash/price
                    qty = float(order['notional']) / snapshot_price[curr_symbol]['latestTrade']['p']

                positions_dict[curr_symbol]['available'] -= qty
                positions_dict[curr_symbol]['hold'] += qty

        # Note that now __unique assets could be uninitialized:
        if self.__unique_assets is None:
            self.init_exchange()

        for i in self.__unique_assets:
            if i not in positions_dict:
                positions_dict[i] = utils.AttributeDict({
                    'available': 0.0,
                    'hold': 0.0
                })

        if symbol is not None:
            if symbol in positions_dict:
                return utils.AttributeDict({
                    'available': float(positions_dict[symbol]['available']),
                    'hold': float(positions_dict[symbol]['hold'])
                })
            else:
                raise KeyError('Symbol not found.')

        if symbol == 'USD':
            return utils.AttributeDict({
                'available': positions_dict['USD']['available'],
                'hold': positions_dict['USD']['hold']
            })

        return positions_dict

    @staticmethod
    def __parse_iso(response):
        from dateutil import parser
        try:
            response['created_at'] = parser.isoparse(response['created_at']).timestamp()
        except ValueError as e:
            if str(e) == 'Unused components in ISO string':
                response['created_at'] = parser.parse(response['created_at']).timestamp()
            else:
                raise e

        return response

    @utils.order_protection
    def market_order(self, symbol, side, size) -> MarketOrder:
        assert isinstance(self.calls, alpaca_trade_api.REST)

        needed = self.needed['market_order']
        order = utils.build_order_info(0, side, size, symbol, 'market')

        response = self.calls.submit_order(symbol, side=side, type='market', time_in_force='day', qty=size)

        response = self._fix_response(needed, response)
        return MarketOrder(order, response, self)

    @utils.order_protection
    def limit_order(self, symbol: str, side: str, price: float, size: float) -> LimitOrder:
        needed = self.needed['limit_order']
        order = utils.build_order_info(price, side, size, symbol, 'limit')

        response = self.calls.submit_order(symbol,
                                           side=side,
                                           type='limit',
                                           time_in_force='gtc',
                                           qty=size,
                                           limit_price=price)

        response = self._fix_response(needed, response)
        return LimitOrder(order, response, self)

    @utils.order_protection
    def take_profit_order(self, symbol: str, price: float, size: float) -> TakeProfitOrder:
        side = 'sell'
        needed = self.needed['take_profit']
        order = utils.build_order_info(price, side, size, symbol, 'take_profit')

        response = self.calls.submit_order(symbol,
                                           side=side,
                                           type='limit',
                                           time_in_force='gtc',
                                           qty=size,
                                           limit_price=price)

        response = self._fix_response(needed, response)
        return TakeProfitOrder(order, response, self)

    @utils.order_protection
    def stop_loss_order(self, symbol: str, price: float, size: float) -> StopLossOrder:
        side = 'sell'
        needed = self.needed['stop_loss']
        order = utils.build_order_info(price, side, size, symbol, 'stop_loss')

        response = self.calls.submit_order(symbol,
                                           side=side,
                                           type='stop',
                                           time_in_force='gtc',
                                           qty=size,
                                           stop_price=price)

        response = self._fix_response(needed, response)
        return StopLossOrder(order, response, self)

    def _fix_response(self, needed, response):
        response = self.__parse_iso(response)
        response = utils.rename_to([
            ['limit_price', 'price'],
            ['qty', 'size']
        ], response)
        response = utils.isolate_specific(needed, response)
        if 'time_in_force' in response:
            response['time_in_force'] = response['time_in_force'].upper()
        return response

    def cancel_order(self, symbol, order_id) -> dict:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        self.calls.cancel_order(order_id)

        # TODO: handle the different response codes
        return {'order_id': order_id}

    def get_open_orders(self, symbol=None):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        if symbol is None:
            orders = self.calls.list_orders(status='open')
        else:
            orders = self.calls.list_orders(status='open', symbols=[symbol])

        for i in range(len(orders)):
            # orders[i] = utils.rename_to(renames, orders[i])
            # if orders[i]['type'] == "limit":
            #     orders[i]['price'] = orders[i]['limit_price']
            # if orders[i]['type'] == "market":
            #     if orders[i]['notional']:
            #         orders[i]['funds'] = orders[i]['notional']
            #     else:
            #         orders[i]['funds'] = orders[i]['notional']
            # orders[i]['created_at'] = parser.isoparse(orders[i]['created_at']).timestamp()
            orders[i] = self.homogenize_order(orders[i])

        return orders

    def get_order(self, symbol, order_id) -> dict:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        order = self.calls.get_order(order_id)
        order = self.homogenize_order(order)
        return order

    # TODO: fix this function
    def homogenize_order(self, order):
        if order['type'] == "limit":
            renames = [
                ["qty", "size"],
                ["limit_price", "price"]
            ]
            order = utils.rename_to(renames, order)
        elif order['type'] == "stop_loss":
            renames = [
                ["qty", "size"],
                ["limit_price", "price"]
            ]
            order = utils.rename_to(renames, order)
        elif order['type'] == "take_profit":
            renames = [
                ["qty", "size"],
                ["limit_price", "price"]
            ]
            order = utils.rename_to(renames, order)
        elif order['type'] == "market":
            if order['notional']:
                renames = [
                    ["notional", "funds"]
                ]
                order = utils.rename_to(renames, order)

            else:  # market order of number of shares
                order['size'] = order.pop('qty')

        # TODO: test stop_limit orders
        elif order['type'] == "stop_limit":
            renames = [
                ["qty", "size"],
            ]
            order = utils.rename_to(renames, order)

        order = self.__parse_iso(order)
        if 'time_in_force' in order:
            order['time_in_force'] = order['time_in_force'].upper()

        needed = self.choose_order_specificity(order['type'])

        order = utils.isolate_specific(needed, order)
        return order

    def get_fees(self, symbol):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        return {
            'maker_fee_rate': 0.0,
            'taker_fee_rate': 0.0
        }

    def get_product_history(self, symbol: str, epoch_start: float, epoch_stop: float, resolution: int):
        if not self.user_preferences['settings']['alpaca']['use_yfinance']:
            assert isinstance(self.calls, alpaca_trade_api.REST)

            resolution = time_interval_to_seconds(resolution)

            supported_multiples = [60, 3600, 86400]
            if resolution not in supported_multiples:
                utils.info_print("Granularity is not an accepted granularity...rounding to nearest valid value.")
                resolution = supported_multiples[min(range(len(supported_multiples)),
                                                     key=lambda i: abs(supported_multiples[i] - resolution))]

            found_multiple, row_divisor = super().evaluate_multiples(supported_multiples, resolution)

            if found_multiple == 60:
                time_interval = TimeFrame.Minute
            elif found_multiple == 3600:
                time_interval = TimeFrame.Hour
            else:
                time_interval = TimeFrame.Day

            epoch_start_str = dt.fromtimestamp(epoch_start, tz=timezone.utc).isoformat()
            epoch_stop_str = dt.fromtimestamp(epoch_stop, tz=timezone.utc).isoformat()

            try:
                try:
                    bars = self.calls.get_bars(symbol, time_interval, epoch_start_str, epoch_stop_str,
                                               adjustment='raw').df
                except TypeError:
                    # If you query a timeframe with no data the API throws a Nonetype issue so just return something
                    #  empty if that happens
                    return pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            except AlpacaAPIError as e:
                if e.code == 42210000:
                    warning_string = "Your alpaca subscription does not permit querying data from the last 15 " \
                                     "minutes. Blankly is adjusting your query."
                    utils.info_print(warning_string)
                    epoch_stop = time.time() - (build_minute() * 15)
                    if epoch_stop >= epoch_start:
                        try:
                            return self.get_product_history(symbol, epoch_start, epoch_stop, resolution)
                        except TypeError:
                            # If you query a timeframe with no data the API throws a Nonetype issue so just
                            #  return something
                            #  empty if that happens
                            return pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                    else:
                        warning_string = "No data range queried after time adjustment."
                        utils.info_print(warning_string)
                        return pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                else:
                    raise e
            bars.rename(columns={"t": "time", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"},
                        inplace=True)

            if bars.empty:
                return pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            return utils.get_ohlcv(bars, row_divisor, from_zero=False)
        else:
            # This runs yfinance on the symbol
            return self.parse_yfinance(symbol, epoch_start, epoch_stop, resolution)

    def overridden_history(self, symbol, epoch_start, epoch_stop, resolution_seconds, **kwargs) -> pd.DataFrame:
        to = kwargs['to']
        # If it's a string alpaca is an edge case where epoch can be used
        if to is not None and isinstance(to, str):
            to = None
        if to:
            if not self.user_preferences['settings']['alpaca']['use_yfinance']:
                resolution_seconds = self.valid_resolutions[min(range(len(self.valid_resolutions)),
                                                                key=lambda j: abs(self.valid_resolutions[j] -
                                                                                  resolution_seconds))]
                resolution_lookup = {
                    60: '1Min',
                    300: '5Min',
                    900: '15Min',
                    86400: '1Day'
                }

                time_interval = resolution_lookup[resolution_seconds]

                def find_last_n_points(epoch_start_, epoch_stop_):
                    frames = []

                    # This just overestimates and then chops off the remainder
                    while epoch_start_ <= epoch_stop_:
                        # Create an end time by moving after the start time by 1000 datapoints
                        frames.append(self.calls.get_bars(symbol, time_interval, limit=10000,
                                                          start=utils.iso8601_from_epoch(epoch_start_)).df)
                        epoch_start_ += resolution_seconds * 10000

                    for i in range(len(frames)):
                        series = []
                        for j in frames[i].index:
                            series.append(j.timestamp())
                        frames[i]['time'] = pd.Series(series).values
                        frames[i] = frames[i].reset_index(drop=True)

                    if len(frames) != 0:
                        response_ = pd.concat(frames, ignore_index=True)
                    else:
                        response_ = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])

                    return response_

                # Create an empty dataframe here
                response = pd.DataFrame(columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                batched_ranges = [epoch_start, epoch_stop]
                # Batch it until we have enough points
                tries = 2
                while len(response) < to:
                    response = pd.concat([response, find_last_n_points(batched_ranges[0], batched_ranges[1])])
                    batched_ranges[0] -= resolution_seconds * tries
                    batched_ranges[1] -= resolution_seconds * tries
                    tries = tries * 2

                response = response[['time', 'open', 'high', 'low', 'close', 'volume']]

                response = response.sort_values(by=['time'], ignore_index=True)

                response = response.tail(to)

                response = response.astype({
                    'time': int,
                    'open': float,
                    'high': float,
                    'low': float,
                    'close': float,
                    'volume': float,
                })
            else:
                # Overestimate the difference for yfinance
                epoch_start = epoch_stop - (epoch_stop - epoch_start) * 1.5

                return self.parse_yfinance(symbol, epoch_start, epoch_stop, resolution_seconds).tail(to).reset_index()
        else:
            response = self.get_product_history(symbol,
                                                epoch_start,
                                                epoch_stop,
                                                int(resolution_seconds))

        return response

    @staticmethod
    def __convert_times(date):  # There aren't any usages of this
        # convert start_date to datetime object
        if isinstance(date, str):
            import dateparser
            date = dateparser.parse(date)
        elif isinstance(date, float):
            date = dt.fromtimestamp(date)

        # end_date object is naive datetime, so need to convert
        if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
            date = date.replace(tzinfo=timezone.utc)

        return date

    def get_order_filter(self, symbol: str):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        current_price = self.get_price(symbol)

        products = self.get_products()

        product = None
        for i in products:
            if i['symbol'] == symbol:
                product = i
                break
        if product is None:
            raise APIException("Symbol not found.")

        exchange_specific = product['exchange_specific']
        fractionable = exchange_specific['fractionable']

        if fractionable:
            quote_increment = 1e-9
            min_funds_buy = 1
            min_funds_sell = 1e-9 * current_price

            # base_min_size = product['base_min_size']
            base_max_size = product['base_max_size']
            # base_increment = product['base_increment']
            min_price = 0.0001
            max_price = 10000000000

            # Guaranteed nano share if fractionable
            base_min_size = 1e-9
            base_increment = 1e-9
        else:
            quote_increment = current_price
            min_funds_buy = current_price
            min_funds_sell = current_price

            # base_min_size = product['base_min_size']
            base_max_size = product['base_max_size']
            # base_increment = product['base_increment']
            min_price = 0.0001
            max_price = 10000000000

            # Always 1 if not fractionable
            base_min_size = 1
            base_increment = 1

        max_funds = current_price * 10000000000

        return {
            "symbol": symbol,
            "base_asset": symbol,
            "quote_asset": 'USD',
            "max_orders": 500,  # More than this and we can't calculate account value (alpaca is very bad)
            "limit_order": {
                "base_min_size": 1,  # Minimum size to buy
                "base_max_size": base_max_size,  # Maximum size to buy
                "base_increment": 1,  # Specifies the minimum increment for the base_asset.

                "price_increment": min_price,  # TODO test this at market open

                "min_price": min_price,
                "max_price": max_price,
            },
            'market_order': {
                "fractionable": fractionable,

                "base_min_size": base_min_size,  # Minimum size to buy
                "base_max_size": base_max_size,  # Maximum size to buy
                "base_increment": base_increment,  # Specifies the minimum increment for the base_asset.

                "quote_increment": quote_increment,  # Specifies the min order price as well as the price increment.
                "buy": {
                    "min_funds": min_funds_buy,
                    "max_funds": max_funds,
                },
                "sell": {
                    "min_funds": min_funds_sell,
                    "max_funds": max_funds,
                },
            },
            "exchange_specific": {
                "id": exchange_specific['id'],
                "class": exchange_specific['class'],
                "exchange": exchange_specific['exchange'],
                "status": exchange_specific['status'],
                "tradable": exchange_specific['tradable'],
                "marginable": exchange_specific['marginable'],
                "shortable": exchange_specific['shortable'],
                "easy_to_borrow": exchange_specific['easy_to_borrow'],
                "price": current_price
            }
        }

    def get_price(self, symbol) -> float:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        response = self.calls.get_latest_trade(symbol=symbol)
        return float(response['p'])

    @staticmethod
    def parse_yfinance(symbol: str, epoch_start: [int, float], epoch_stop: [int, float], resolution: int):
        try:
            import yfinance

            start_date = dt.fromtimestamp(epoch_start, tz=timezone.utc)
            stop_date = dt.fromtimestamp(epoch_stop, tz=timezone.utc)
            ticker = yfinance.Ticker(symbol)
            result = ticker.history(start=start_date, end=stop_date, interval=number_interval_to_string(resolution))

            result['time'] = result.index.astype(int) // 10 ** 9
            result = result[['Open', 'High', 'Low', 'Close', 'Volume', 'time']].reset_index()

            result = result.rename(columns={
                'time': 'time',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            result = result[['time', 'open', 'high', 'low', 'close', 'volume']]

            return result
        except ImportError:
            raise ImportError("To use yfinance to download data please pip install yfinance")
