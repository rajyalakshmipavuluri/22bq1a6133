from flask import request

def logging_middleware(app):
    # Logging the incoming requests
    @app.before_request
    def _log_incoming():
        method = request.method
        path = request.path
        try:
            body = request.get_json(force=False, silent=True)
        except Exception:
            body = None
        app.logger.info(f"Request: method={method}, path={path}, body={body}")

    # Logging the outgoing responses
    @app.after_request
    def _log_outgoing(response):
        status = response.status
        data = response.get_data(as_text=True)
        app.logger.info(f"Response: status={status}, data={data}")
        return response

    # Logging teardown events (if errors occur)
    @app.teardown_request
    def _log_teardown(error=None):
        if error is not None:
            app.logger.error(f"Teardown error: {error}")
