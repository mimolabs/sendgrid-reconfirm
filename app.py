import time
import redis
import json
import requests

from flask import Flask, render_template, request
import config as config

application = Flask(__name__)

cache = redis.Redis(host=config.REDIS_URL, port=6379)

def process(email):
    url = "https://api.sendgrid.com/v3/contactdb/recipients"
    headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer ' + config.SENDGRID_TOKEN
            }

    body = [{'email': email}]
    r = requests.post(url, headers=headers, json=body)

    recipient = None
    if r.status_code is not 201:
        print('Invalid response')
    else:
        print('Found email added or discovered')
        data = json.loads(r.text)

        if 'persisted_recipients' in data.keys() and len(data['persisted_recipients']) > 0:
            recipient = data['persisted_recipients'][0]#.decode('utf-8')

    if recipient is not None:
        url = "https://api.sendgrid.com/v3/contactdb/lists/{}/recipients/{}".format(config.NEW_LIST, recipient)
        r = requests.post(url, headers=headers, json=body)
        if r.status_code is not 201:
            print('Error adding {} to list {}'.format(email, config.NEW_LIST))
        else:
            print('Adding {} to list {}'.format(email, config.NEW_LIST))

        url = "https://api.sendgrid.com/v3/contactdb/lists/{}/recipients/{}".format(config.OLD_LIST, recipient)
        r = requests.delete(url, headers=headers, json=body)

        if r.status_code is not 201:
            print('Error deleting {} from list {}'.format(email, config.OLD_LIST))
        else:
            print('Deleting {} from list {}'.format(email, config.OLD_LIST))


@application.route("/")
def index():
    email = request.args.get('email')
    if email is None:
        print('No email')
    else:
        val = cache.get(email)
        if val is None:
            print('Importing email to lists')
            process(email)
            # cache.set(email, time.time())
        else:
            print('{} already processed'.format(email))

    return render_template('./index.html', email=email)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
