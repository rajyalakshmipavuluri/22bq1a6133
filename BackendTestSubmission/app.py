from flask import Flask, request, jsonify, redirect
from models import db, ShortURL
from LogginMiddleware.middleware import logging_middleware
import string, random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
db.init_app(app)

logging_middleware(app)

# Utility to Generate shortcode if not provided
def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Create Shortcode URL for given URL
@app.route("/shorturls", methods=["POST"])
def create_short_url():
    data = request.get_json()
    url = data.get("url")
    shortcode = data.get("shortcode")
    validity = data.get("validity", 30)  # default 30 minutes

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Handle shortcode
    if shortcode:
        if not shortcode.isalnum():
            return jsonify({"error": "Shortcode must be alphanumeric"}), 400
        if ShortURL.query.filter_by(shortcode=shortcode).first():
            return jsonify({"error": "Shortcode already exists"}), 409
    else:
        shortcode = generate_shortcode()

    expires_at = datetime.utcnow() + timedelta(minutes=validity)

    short_url = ShortURL(original_url=url, shortcode=shortcode, expires_at=expires_at)
    db.session.add(short_url)
    db.session.commit()

    return jsonify({
        "shortUrl": f"http://localhost:5000/{shortcode}",
        "expiresAt": expires_at.isoformat()
    }), 201


# Route to handle redirection using shortcode
@app.route("/<shortcode>", methods=["GET"])
def handle_redirect(shortcode):
    url_entry = ShortURL.query.filter_by(shortcode=shortcode).first()
    if url_entry is None:
        return jsonify({"error": "No such shortcode exists."}), 404
    if url_entry.is_expired():
        return jsonify({"error": "This shortcode has expired."}), 410
    return redirect(url_entry.original_url)

# Custom error handler for bad requests
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "Invalid request received."}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
