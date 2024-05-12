import random
import csv
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Qusasat():
    def __init__(self, categories_file, quotes_file):
        self._categories = self._load_data(file_name=categories_file)
        self._quotes = self._load_data(file_name=quotes_file)
        self._quote_keys = list(self._quotes.keys())

    @staticmethod
    def _load_data(file_name):
        line_count = 0
        data = {}
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    header = row
                    logger.debug(f'Header found: {header}')
                    line_count += 1
                else:
                    data[row[0]] = {k: v for k, v in zip(header, row)}
                    line_count += 1
            logger.info(f'Loaded {line_count} records from {file_name}')
        return data

    def _get_quote_object(self, quote_id):
        quote = self._quotes.get(quote_id)
        if quote is None:
            return None
        category = self._categories[quote['category']]
        return {
            'id': quote_id,
            'quote': quote['qusasa'],
            'category': category['category']
        }

    def get_random_quote(self):
        random_quote_id = random.choice(self._quote_keys)
        return self._get_quote_object(random_quote_id)

    def get_quote(self, quote_id):
        return self._get_quote_object(quote_id)
