import os
from app import setup

app=setup()

if __name__ == "__main__": 
    app.run(threaded=True, host='0.0.0.0', port=int(os.getenv('APP_PORT')))
