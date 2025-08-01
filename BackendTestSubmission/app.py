from flask import Flask, request, jsonify
from LoggingMiddleware.middleware import logging_middleware

app = Flask(__name__)

logging_middleware(app)




if __name__ == "__main__":
    app.run(port=5000 ,debug=True)