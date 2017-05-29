from flask_script import Manager
from web import app

cli = Manager(app)

@cli.command
def web():
    """
    Run the web server
    """
    print('Running server...')
    app.run(debug=True)
