from flask import Flask, jsonify, render_template, abort
from qusasat import Qusasat
import base64


app = Flask(__name__)
qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')

# Load the only image we have as base64 data in memory
with open('static/paper.png', 'rb') as file:
    file_data = file.read()
base64_data = base64.b64encode(file_data)
base64_string = base64_data.decode('utf-8')

def lambda_root(event, context):
    return root_html()

@app.route('/')
def root_html():
    global base64_string
    quote = qusasat.get_random_quote()
    return render_template('quote.html', 
                            category=quote['category'],
                            quote=quote['quote'],
                            background_image_url=f'data:image/png;base64,{base64_string}')

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
