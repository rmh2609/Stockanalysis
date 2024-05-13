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

class TestReadMetadataFromCSV(unittest.TestCase):
    def test_read_metadata_from_csv(self):
            # Provide a sample CSV file for testing
        data = read_metadata_from_csv('metadata.csv')
            # Add assertions to verify the correctness of the output
        self.assertEqual(data['AAPL'], 'Apple Inc.')
        self.assertEqual(data['GOOGL'], 'Alphabet Inc.')
        self.assertEqual(data['MSFT'], 'Microsoft Corp.')
        self.assertEqual(data['AMZN'], 'Amazon.com Inc.')

class TestReadPricesFromExcel(unittest.TestCase):
    def test_read_prices_from_excel(self):
        # Test file containing sample data
        test_file = 'trades_update.xlsx'

        # Expected output
        expected_prices = {
            'AAPL': {
                '2021-01-01': 132.05,
                '2021-01-02': 134.00,
                '2021-01-03': 131.50,
                '2021-01-04': 130.00,
                '2021-01-05': 129.00,
                '2021-01-07': 1730.00,
                '2021-01-08': 132.50
            },
            'GOOGL': {
                '2021-01-02': 1733.18,
                '2021-01-01': 1728.24,
                '2021-01-04': 1740.92,
                '2021-01-09': 1720.00,
                '2021-01-07': 1730.00
            },
            'MSFT': {
                '2021-01-03': 224.97,
                '2021-01-03': 225.95,
                '2021-01-06': 230.00,
                '2021-01-09': 235.00
            },
            'AMZN': {
                '2021-01-03': 3228.44,
                '2021-01-02': 3206.20,
                '2021-01-05': 3210.00,
                '2021-01-10': 3240.00,
                '2021-01-07': 3230.00
                    }
                }

        # Call the function
        prices = read_prices_from_excel(test_file)
        print(prices)
        print(read_prices_from_excel(test_file))




import csv
import openpyxl
from typing import Dict

def read_metadata_from_csv(filename: str) -> Dict[str, str]:
    """
    Reads stock metadata from a CSV file.

    :param filename: str, path to the CSV file containing stock metadata
    :return: Dict[str, str], a dictionary mapping stock tickers to company names
    """
    output = {}
    with open(filename, 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Read the CSV data
        for row in csv_reader:

            ticker = row.get('Ticker')
            company = row.get('CompanyName')

            if ticker != "Ticker":
                output[ticker] = company

    return output

import pandas as pd

def read_prices_from_excel(filename: str) -> Dict[str, Dict[str, float]]:
    """
    Reads historical stock prices from an Excel file.

    :param filename: str, path to the Excel file containing historical prices
    :return: Dict[str, Dict[str, float]], a nested dictionary where the first key is the stock ticker,
             and the second key is the date, with prices as float values.
    """
    df = pd.read_excel(filename)

    if 'Ticker' not in df.columns or 'TradeDate' not in df.columns or 'Price' not in df.columns:
            raise ValueError("Required columns ('Ticker', 'TradeDate', 'Price') not found in the Excel file.")
    prices = {}

    for index, row in df.iterrows():
        ticker = row['Ticker']
        date = str(row['TradeDate']).split()[0]

        price = row['Price']

        if ticker not in prices:
            prices[ticker] = {}

        prices[ticker][date] = price


    return prices

def create_and_load_stocks(metadata_file: str,
                           	prices_file: str) -> StockCollection:
    """
    Creates StockData objects from metadata and prices files,
    then loads them into a StockCollection.

    This function should use the above 2 helper functions.

    :param metadata_file: str, path to the CSV file with stock metadata
    :param prices_file: str, path to the Excel file with historical prices
    :return: StockCollection, a collection of loaded stocks
    """
    collection = StockCollection()

    metadata = read_metadata_from_csv(metadata_file)
    prices = read_prices_from_excel(prices_file)

    mapping = defaultdict(StockData)

    for ticker,company in metadata.items():
        if ticker in prices:
            data = StockData(ticker,company, prices[ticker])
            collection.add_stock_data(data)
    return collection



def write_summary_csv(stock_collection: StockCollection, output_file: str) -> None:
    """
    Writes a summary CSV file with each stock's ticker,
    	company name, and the number of historical price entries.
	Before writing to a CSV, you should sort it by the number of days
    there are price entries.

    :param stock_collection: StockCollection, the collection of stocks to summarize
    :param output_file: str, the path to the output CSV file
    """
    summary_data = []
    for stock_data in stock_collection.stocks.values():
        ticker = stock_data.ticker
        company_name = stock_data.company_name
        number_of_days = stock_data.days_of_data()
        summary_data.append((ticker, company_name, number_of_days))

    # Sort the list of tuples by number_of_days
    summary_data.sort(key=lambda x: x[2])

    # Write the sorted list of tuples to the CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ticker', 'Company Name', 'Number of Days'])
        writer.writerows(summary_data)


if __name__ == '__main__':
    unittest.main()
