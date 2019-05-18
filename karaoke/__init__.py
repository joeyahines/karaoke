import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        UPLOAD_FOLDER="upload"
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # apply the blueprints to the app
    from karaoke import convert

    app.register_blueprint(convert.bp)

    app.add_url_rule("/", endpoint="index")

    return app
