import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import json

from amazon_api import app


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Api scriping Amazon Dodee</h1>
<p>Api creata appositamente per scraping di prodotti presenti sul marketplace amazon per la piattaforma dodee.it</p>'''




@app.route('/api/v1/asinLookUp/product', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'asin' in request.args:
        id = str(request.args['asin'])
    else:
        return "Error: No asin field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Preparing Amazon link
    URL = 'https://www.amazon.it/gp/product/' + id

    # Printing url for debug
    print(URL)

    # AMAZON SCRAPE STUFF
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find_all(id="priceblock_ourprice")[0].get_text().replace('\u00a0\u20ac', '')
    features = []
    for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
        features.append(li.get_text().strip())

    img = soup.find("div", {"id": "imgTagWrapperId"}).find("img")
    data = json.loads(img["data-a-dynamic-image"])
    image = list(data.keys())[1]
    print(title)
    print(price.replace('\u00a0\u20ac', ''))



    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(title=title,
                   price=price,
                   features=features,
                   image=image
                   )

app.run()
