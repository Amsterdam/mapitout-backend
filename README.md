# mapitout-backend
backend services for map it out app

Required environment variables:
```
APP_ID : travel time api id
APP_KEY : travel time api key
```

#### Local development ####
```
virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install -r requirements.txt
```
#### Run ####
```
export APP_ID=<id>
export APP_KEY=<key>
export FLASK_APP=proxy-server.py
flask run
```
