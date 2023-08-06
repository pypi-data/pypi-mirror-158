"""
    Keyless interface definition
    Copyright (C) 2022 Emerson Dove

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
import pandas as pd


from blankly.exchanges.interfaces.exchange_interface import ExchangeInterface
from blankly.exchanges.orders.limit_order import LimitOrder
from blankly.utils.utils import AttributeDict, get_base_asset, get_quote_asset, aggregate_prices_by_resolution, \
    extract_price_by_resolution


# This just happens to also inherit from the exchange interface
class KeylessAPI(ExchangeInterface):
    def __init__(self, maker_fee, taker_fee, price_readers):
        if not isinstance(price_readers, list):
            price_readers = [price_readers]

        self.__final_prices = {}
        prices: dict = {}

        for price_reader in price_readers:
            data = price_reader.data
            for symbol in data:
                symbol_info = price_reader.prices_info[symbol]
                resolution = symbol_info['resolution']

                # Add each symbol to the final prices without doing any processing
                if symbol in prices:
                    prices[symbol] = pd.concat([prices[symbol], data[symbol]])
                else:
                    prices[symbol] = data[symbol]

                self.__final_prices = aggregate_prices_by_resolution(self.__final_prices, symbol, resolution,
                                                                     data[symbol])

        self.__products = None
        self.__accounts = None

        self.fees = {
            'maker_fee_rate': maker_fee,
            'taker_fee_rate': taker_fee
        }

        super().__init__('keyless', self)

    def init_exchange(self):
        pass

    def __invalid_live(self):
        raise RuntimeError("Cannot use a keyless exchange in live trading. Please insert keys and begin using exchanges"
                           " such as blankly.Alpaca() or blankly.CoinbasePro().")

    def get_exchange_type(self):
        return 'keyless'

    def get_account(self, symbol: str = None) -> AttributeDict:
        return AttributeDict(self.__accounts)

    def get_product_history(self, symbol, epoch_start, epoch_stop, resolution):
        return extract_price_by_resolution(self.__final_prices, symbol, epoch_start, epoch_stop, resolution)

    def get_products(self):
        self.__invalid_live()

    def market_order(self, symbol: str, side: str, size: float):
        self.__invalid_live()

    def take_profit_order(self, symbol: str, price: float, size: float):
        self.__invalid_live()

    def stop_loss_order(self, symbol: str, price: float, size: float):
        self.__invalid_live()

    def limit_order(self, symbol: str, side: str, price: float, size: float):
        self.__invalid_live()

    def cancel_order(self, symbol: str, order_id: str):
        self.__invalid_live()

    def get_open_orders(self, symbol: str = None):
        self.__invalid_live()

    def get_order(self, symbol: str, order_id: str):
        self.__invalid_live()

    def get_fees(self, symbol) -> dict:
        return self.fees

    def get_order_filter(self, symbol: str) -> dict:
        return {
            "symbol": symbol,
            "base_asset": get_base_asset(symbol),
            "quote_asset": get_quote_asset(symbol),
            "max_orders": 1000000000000000,
            "limit_order": {
                "base_min_size": 0.000000001,  # Minimum size to buy
                "base_max_size": 1000000000000000,  # Maximum size to buy
                "base_increment": 0.000000001,  # Specifies the minimum increment
                # for the base_asset.
                "price_increment": 0.000000001,

                "min_price": 0.000000001,
                "max_price": 1000000000000000,
            },
            'market_order': {
                "fractionable": True,

                "base_min_size": 0.000000001,  # Minimum size to buy
                "base_max_size": 1000000000000000,  # Maximum size to buy
                "base_increment": 0.000000001,  # Specifies the minimum increment

                "quote_increment": 0.000000001,  # Specifies the min order price as well
                # as the price increment.
                "buy": {
                    "min_funds": 0.000000001,
                    "max_funds": 1000000000000000,
                },
                "sell": {
                    "min_funds": 0.000000001,
                    "max_funds": 1000000000000000,
                },
            },
            "exchange_specific": {}
        }

    def get_price(self, symbol: str, time=None):
        self.__invalid_live()


