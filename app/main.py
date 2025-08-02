from flask import Flask, request, jsonify, redirect
from app.utils import generate_short_code
from app.models import init_db, insert_url, get_url, increment_visit_count, get_stats

app = Flask(__name__)
init_db()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API with DB"
    })

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    insert_url(short_code, original_url)

    short_url = request.host_url + short_code
    return jsonify({
        'original_url': original_url,
        'short_code': short_code,
        'short_url': short_url
    })

@app.route('/<short_code>')
def redirect_to_original(short_code):
    result = get_url(short_code)
    if result:
        original_url, _ = result
        increment_visit_count(short_code)
        return redirect(original_url)
    else:
        return jsonify({'error': 'Invalid short code'}), 404

@app.route('/stats/<short_code>')
def stats(short_code):
    result = get_stats(short_code)
    if result:
        original_url, visit_count = result
        return jsonify({
            'original_url': original_url,
            'short_code': short_code,
            'visit_count': visit_count
        })
    else:
        return jsonify({'error': 'Short code not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
