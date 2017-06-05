from flask_script import Manager
from web import app
import os

cli = Manager(app)

@cli.command
def web():
    """
    Run the web server
    """
    print('Running server...')
    port = os.environ['PORT']

    app.run(host='0.0.0.0', port=port)
