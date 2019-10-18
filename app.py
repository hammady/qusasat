from flask import Flask, jsonify, render_template, abort
from qusasat import Qusasat


app = Flask(__name__)
qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')

@app.route('/')
def root_html():
    quote = qusasat.get_random_quote()
    return render_template('quote.html', category=quote['category'], quote=quote['quote'])

@app.route('/.json')
def root_json():
    quote = qusasat.get_random_quote()
    return jsonify(quote)

@app.route('/<int:quote_id>')
def get_quote_html(quote_id):
    quote = qusasat.get_quote(str(quote_id))
    if quote is None:
        return abort(404)
    else:
        return render_template('quote.html', category=quote['category'], quote=quote['quote'])

@app.route('/<int:quote_id>.json')
def get_quote_json(quote_id):
    quote = qusasat.get_quote(str(quote_id))
    if quote is None:
        return jsonify({'status': 'Not Found'}), 404
    else:
        return jsonify(quote)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
