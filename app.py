# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)
# CORS(app)  # Enable CORS to allow requests from React frontend

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     data = request.get_json()
#     url = data.get('url')
#     if not url:
#         return jsonify({"error": "URL parameter is required"}), 400

#     try:
#         r = requests.get(url)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         paragraphs = soup.find_all('p')

#         extracted_text = ' '.join([p.text.strip() for p in paragraphs])

#         return jsonify({"content": extracted_text})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def extract_text_from_html(html):
    """Extracts and formats text from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.extract()

    # Extract structured text
    text_blocks = []
    for tag in soup.find_all("p"):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            text_blocks.append(text)

    # Combine text with new lines for readability
    return "\n\n".join(text_blocks)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        r = requests.get(url)
        extracted_text = extract_text_from_html(r.text)
        
        return jsonify({"content": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
