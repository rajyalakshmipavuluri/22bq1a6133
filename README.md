## URL Shortener Flask Application

This project is a simple URL shortener built using Python and the Flask web framework. It allows users to create short, unique codes for long URLs, making them easier to share and manage. The application also supports setting an expiration time for each shortened URL.

### Features

- Shorten any valid URL to a custom or randomly generated shortcode
- Set a validity period (in minutes) for each shortened URL
- Redirect users to the original URL when the shortcode is accessed
- Handles errors such as invalid input, duplicate shortcodes, and expired links
- Logs all requests and responses for monitoring

### How It Works

1. The user sends a POST request with a URL (and optionally a custom shortcode and validity period).
2. The application stores the original URL, shortcode, and expiration time in a SQLite database.
3. When someone visits the short URL, the app checks if the shortcode exists and is still valid, then redirects to the original URL.
4. If the shortcode is invalid or expired, the app returns an appropriate error message.

### Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy (for database management)
- SQLite (as the database)

### Getting Started

1. Clone the repository to your local machine.
2. Set up a Python virtual environment and install the required packages.
3. Run the Flask application.
4. Use tools like Postman or curl to interact with the API endpoints.

### API Endpoints

- `POST /shorturls` - Create a new short URL. Requires a JSON body with the `url` field. Optional fields: `shortcode`, `validity` (in minutes).
- `GET /<shortcode>` - Redirects to the original URL if the shortcode is valid and not expired.

### Example Request

```
POST /shorturls
{
  "url": "https://www.example.com",
  "shortcode": "mycode",
  "validity": 60
}
```

### Notes

- The application uses a simple logging middleware to record all incoming requests and outgoing responses.
- All configuration is done in the `app.py` file.
- The database file (`urls.db`) will be created automatically in the project directory.

This project is intended for learning and demonstration purposes. It can be extended with features like user authentication, analytics, or a web interface.
