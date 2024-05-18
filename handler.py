from flask import Flask, render_template
from qusasat import Qusasat
import base64

app = Flask(__name__)
# Load data
qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')
# Load the only image we have as base64 data in memory
with open('static/paper.png', 'rb') as file:
    file_data = file.read()
base64_data = base64.b64encode(file_data)
base64_string = base64_data.decode('utf-8')

def run(event, context):
    global app, qusasat, base64_string
    quote = qusasat.get_random_quote()
    with app.app_context():
        body = render_template('quote.html', 
                                category=quote['category'],
                                quote=quote['quote'],
                                background_image_url=f'data:image/png;base64,{base64_string}')
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": body
    }
