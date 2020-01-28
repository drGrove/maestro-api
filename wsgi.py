import os
from maestro_api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=os.environ.get('APP_HOST'), port=os.environ.get('APP_PORT'))
