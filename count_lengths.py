from qusasat import Qusasat
from tweet_poster import TweetPoster

qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')
more_280 = 0
total = 0
for i in range(1, 1000):
    quote = qusasat.get_quote(str(i))
    if quote is None:
        continue
    total = total + 1
    category = quote['category']
    normalized = TweetPoster.to_hashtag(category)
    length = len(quote['quote']) + len(normalized) + 1
    if length > 280:
        more_280 = more_280 + 1
    if len(category) + 1 != len(normalized):
        print(category, '->', normalized)

print('{:d} quotes ({:f}%) have more than 280 characters including normalized categories'.
    format(more_280, more_280 * 100.0 / total))
