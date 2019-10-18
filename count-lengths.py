from qusasat import Qusasat

qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')
more_280 = 0
for i in range(1, 1000):
    quote = qusasat.get_quote(str(i))
    if quote is None:
        break
    length = len(quote['quote']) + len(quote['category']) + 2
    if length > 280:
        more_280 = more_280 + 1

print(more_280)
