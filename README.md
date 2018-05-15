# Reconfirm Consent for your SendGrid Lists

GDPR approaches and we were forced to ask everyone on our list to reconfirm their email. SendGrid recommend doing this on a regular basis anyway.

There were no fast ways to do so using the standard tools so we built this.

It will add an email to a new list and remove from the old one - you can later on delete the first list.

### Steps

1. Create a new SendGrid list - your new clean one
2. Clone this repo
3. Get your new and existing list IDs
4. Deploy it to Heroku (easiest)

#### SendGrid Stuff

Create a new list by adding a new contact manually. Ensure you checked 'Add contacts and include in a new list'.

Get the listID - it's in the URL.

Create another list that includes all your contacts. Get the listID - it's also in the URL.

Get your API token - the docs for this can be found [here](https://sendgrid.com/docs/User_Guide/Settings/api_keys.html)

#### Deploy your own instance using Heroku

Create a Heroku account if you haven't, then grab the source using git:

```
$ git clone git://github.com/mimolabs/sendgrid-reconfirm.git
```

From the project directory, create a Heroku application:

```
$ heroku create
```

Add Heroku's redis addon:

```
$ heroku addons:add heroku-redis
```

Set your environment variables, where NEW_LIST is your new clean list and OLD_LIST is the one you need to remove emails from.

```
$ heroku config:set SENDGRID_TOKEN=SG...... OLD_LIST=xxx NEW_LIST=xxx
```

Now just deploy via git:

```
$ git push heroku master
```

It will push to Heroku and give you a URL you can use in your campaigns.

## Add to your next campaign.

Just add the following link to your next campaign!

https://xxx.heroku.com?email=[%email%]

Make sure you update with your own heroku URL.

## Deploy your own instance using Docker
On the server/machine you want to host this, you'll first need a machine with docker and docker-compose installed, then grab the RequestBin source using git:

```
$ git clone git://github.com/mimolabs/sendgrid-reconfirm.git
```

Go into the project directory and then build and start the containers

```
$ sudo docker-compose build
$ sudo docker-compose up -d
```

# Contributors
Simon Morley simon@polkaspots.com
