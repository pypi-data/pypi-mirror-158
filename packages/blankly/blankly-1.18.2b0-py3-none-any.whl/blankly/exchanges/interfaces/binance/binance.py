"""
    binance exchange definitions and setup
    Copyright (C) 2021  Emerson Dove

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

from binance.client import Client

from blankly.exchanges.exchange import Exchange
from blankly.exchanges.auth.auth_constructor import AuthConstructor
from blankly.utils import utils


class Binance(Exchange):
    def __init__(self, portfolio_name=None, keys_path="keys.json", settings_path=None):
        Exchange.__init__(self, "binance", portfolio_name, settings_path)

        # Load the auth from the keys file
        auth = AuthConstructor(keys_path, portfolio_name, 'binance', ['API_KEY', 'API_SECRET', 'sandbox'])

        sandbox = super().evaluate_sandbox(auth)

        if sandbox:
            calls = Client(api_key=auth.keys['API_KEY'], api_secret=auth.keys['API_SECRET'],
                           tld=self.preferences["settings"]['binance']["binance_tld"],
                           testnet=True)
        else:
            calls = Client(api_key=auth.keys['API_KEY'], api_secret=auth.keys['API_SECRET'],
                           tld=self.preferences["settings"]['binance']["binance_tld"])

        # Always finish the method with this function
        super().construct_interface_and_cache(calls)

    """
    Builds information about the symbol on this exchange by making particular API calls
    """

    def get_asset_state(self, symbol):
        """
        Portfolio state is the internal properties for the exchange block.
        """
        # TODO Populate this with useful information
        symbol = utils.get_base_asset(symbol)
        account = self.interface.get_account(symbol=symbol)
        return account

    def get_exchange_state(self):
        """
        Exchange state is the external properties for the exchange block
        """
        # TODO Populate this with useful information
        return self.interface.get_products()

    def get_direct_calls(self) -> Client:
        return self.calls
