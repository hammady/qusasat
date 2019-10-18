# qusasat

A web app to show a random qusasa (quote) from the book entitled:
Quotes worth burning (قصاصات قابلة للحرق) for the renowned author
[Dr. Ahmed Khalid Tawfik](https://en.wikipedia.org/wiki/Ahmed_Khaled_Tawfik).

Included is a script (`tweet_poster.py`) that automatically posts a tweet with a random quote.

## System requirements
1. [Docker](https://docs.docker.com/install/)
2. There is no number 2!

## Development

### Build

```bash
docker build . -f dev.dockerfile -t qusasat:dev
```

### Run the web app

```bash
docker run -it --rm -p 5000:5000 -v $PWD:/home qusasat:dev
```

Then point your browsear to 
[http://localhost:5000](http://localhost:5000) to get a random quote.
The following routes are available:
- [/](http://localhost:5000/): Return a random quote
- [/.json](http://localhost:5000/.json): Return a random quote in JSON format
- [/\<id\>](http://localhost:5000/1): Return a specific quote by its ID
- [/\<id\>.json](http://localhost:5000/1.json): Return a specific quote by its ID in JSON format

Note that in development mode, editing and saving any file will
refresh the development server automatically and you can refresh
the browser to get your updates.

## Production

### Build

```bash
docker build . -t qusasat:prod
```

### Run the web app

```bash
docker run -it --rm -p 5000:5000 qusasat:prod
```

### Heroku support
The app supports [Heroku](https://www.heroku.com/) out of the box.
Follow the instructions [here](https://devcenter.heroku.com/articles/container-registry-and-runtime)
to deploy this web app using Docker.

## Posting tweets

Run the `tweet_poster.py` script after providing some environment variables:

```bash
docker run -it --rm --env-file .env qusasat:prod python tweet_poster.py
```

Where `.env` contains the following twitter tokens:

```
TWITTER_CONSUMER_KEY=???
TWITTER_CONSUMER_SECRET=???
TWITTER_ACCESS_KEY=???
TWITTER_ACCESS_SECRET=???
```

On Heroku, you can supply those tokens using app
[config vars](https://devcenter.heroku.com/articles/config-vars).
To automatically send scheduled tweets, provision the
[Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) add-on,
and set its command to: `python tweet_poster.py`.
