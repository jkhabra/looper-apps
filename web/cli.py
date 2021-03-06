from flask_script import Manager
from web.app import app
import os

cli = Manager(app)

@cli.command
def web():
    """
    Run the web server
    """
    print('Running server...')
    #port = os.environ['PORT']

    #app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', debug=True)
