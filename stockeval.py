from typing import Optional, Dict

class StockData:
    """Represents a single stock's metadata and historical pricing."""

    def __init__(self, ticker: str, company_name: str,
                 historical_prices: Dict[str, float]):
        """
        Initializes a StockData object with ticker,
        company name, and historical prices.

        :param ticker: str, the stock's ticker symbol
        :param company_name: str, the name of the company
        :param historical_prices: Dictionary the historical price data
        """
        self.ticker = ticker
        self.company_name = company_name
        self.historical_prices = historical_prices


    def days_of_data(self) -> int:
      """
      retutnr the number of days there is historical data.
      """
      return len(self.historical_prices.keys())

    def __str__(self) -> str:
        """
        Returns a string representation of the stock data.
        E.g.
        "(AAPL, Apple Inc.) 1000 price entries"
        1000 is the number price entries
        """
        return self.ticker + ", " + self.company_name + " " + str(self.days_of_data()) + "price entries"


class StockCollection:
    """Manages a collection of StockData objects."""

    def __init__(self):
        """Initializes a new StockCollection with an empty dictionary of stocks."""
        self.stocks: Dict[str, StockData] = {}

    def add_stock_data(self, stock_data: StockData) -> None:
        """
        Adds a StockData object to the collection.

        :param stock_data: StockData, the stock data to add
        """

        self.stocks[stock_data.ticker] = StockData
        return


    def remove_stock_data(self, ticker: str) -> None:
        """
        Removes a StockData object from the collection by ticker.

        :param ticker: str, the ticker symbol of the stock to remove
        """
        self.stocks.remove(ticker)


    def get_stock_data(self, ticker: str) -> Optional[StockData]:
        """
        Retrieves a StockData object by ticker.

        :param ticker: str, the ticker symbol of the stock to retrieve
        :return: Optional[StockData], the StockData object if found, otherwise None
        """
        
        if ticker not in self.stocks:
            return None
        return self.stocks[ticker]


    def __str__(self) -> str:
        """
        Returns a string representation of the collection.
        Just returns a list of the stocks and tickers in the format
        (AAPL, Apple)
        """
        for ticker in self.stocks.keys():
            print(ticker, self.stocks[ticker].company_name)
        return

# Create historical prices for Apple
apple_prices = {
    '2021-01-01': 132.05,
    '2021-01-02': 134.00,
    '2021-01-03': 131.50
}

apple_stock = StockData('AAPL', 'Apple Inc.', apple_prices)

# Will use the `__str__` method to print. Should be
# (AAPL, Apple Inc.) 3 price entries
print(apple_stock)

stock_collection = StockCollection()
stock_collection.add_stock_data(apple_stock)

# Retrieve Apple's stock data from the collection
retrieved_apple_stock = stock_collection.get_stock_data('AAPL')

if retrieved_apple_stock:
    print("Retrieved:", retrieved_apple_stock)
else:
    print("Stock data for AAPL not found.")

import unittest
class TestStockData(unittest.TestCase):

    def setUp(self):
        """Set up test variables for each test."""
        self.historical_prices = {'2021-01-01': 132.05, '2021-01-02': 134.00, '2021-01-03': 131.50}
        self.stock = StockData('AAPL', 'Apple Inc.', self.historical_prices)

    def test_initialization(self):
        """Test initialization of StockData."""
        self.assertEqual(self.stock.ticker, 'AAPL')
        self.assertEqual(self.stock.company_name, 'Apple Inc.')
        self.assertEqual(self.stock.historical_prices, self.historical_prices)

    def test_str(self):
        """Test the string representation of StockData."""
        expected_string = "AAPL, Apple Inc. 3price entries"
        self.assertEqual(str(self.stock), expected_string)

if __name__ == '__main__':
    unittest.main()
