from os import environ as env
import string
from qusasat import Qusasat
import tweepy


class TweetPoster():
    def __init__(self, twitter_config, qusasat, dry_run=False):
        self._qusasat = qusasat
        auth = tweepy.OAuthHandler(
            twitter_config['CONSUMER_KEY'],
            twitter_config['CONSUMER_SECRET']
        )
        auth.set_access_token(
            twitter_config['ACCESS_KEY'],
            twitter_config['ACCESS_SECRET']
        )
        self._api = tweepy.API(auth)
        self._dry_run = dry_run
        self._max_tweet_length = 280
        self._ellipsis = u'\u2026'

    def post(self):
        response_jsons = []
        in_reply_to = None
        long_quote = self._qusasat.get_random_quote()
        for quote in self._split_quote(long_quote):
            formatted = self._format_quote(quote)
            print('About to tweet {} characters: {}'.format(len(formatted), formatted))
            if not self._dry_run:
                response = self._api.update_status(status=formatted,
                                        in_reply_to_status_id=in_reply_to)
                json = response._json
            else:
                json = {'id_str': '0'}
            response_jsons.append(json)
            in_reply_to = json['id_str']
        return response_jsons

    def _split_quote(self, quote):
        hashtag = self.to_hashtag(quote['category'])
        quotes = []
        current_quote = ""
        max_length = self._max_tweet_length - len(self._ellipsis) * 2
        remaining_length = max_length - len(hashtag) - len('\n')
        # we process the words in reverse order so that the first iteration
        # (last quote) contains the hashtag where we can make room for it easily
        # otherwise, we cannot easily identify the last tweet before running
        # out of max length at which point the hashtag may not fit
        for word in quote['quote'].split()[::-1]: # no arguments split on whitespaces
            spaced_word = word + ' ' if current_quote != "" else word
            if len(spaced_word) < remaining_length:
                current_quote = spaced_word + current_quote
                remaining_length -= len(spaced_word)
            else:
                quotes.append({'quote': self._ellipsis + current_quote})
                current_quote = word + self._ellipsis
                remaining_length = max_length - len(current_quote)
        quotes.append({'quote': current_quote})
        quotes[0]['hashtag'] = hashtag
        return reversed(quotes) # reverse quotes to maintain the correct order again

    def _format_quote(self, quote):
        if quote.get('hashtag'):
            return '{}\n{}'.format(quote['quote'], quote['hashtag'])
        else:
            return quote['quote']

    @classmethod
    def to_hashtag(cls, input_string):
        simplified = input_string.translate(str.maketrans('', '', string.punctuation))
        return '#{}'.format(simplified.replace(' ', '_'))


if __name__ == '__main__':
    qusasat = Qusasat(categories_file='./data/categories.csv', quotes_file='./data/qusasat.csv')
    twitter_config = {
        'CONSUMER_KEY': env['TWITTER_CONSUMER_KEY'],
        'CONSUMER_SECRET': env['TWITTER_CONSUMER_SECRET'],
        'ACCESS_KEY': env['TWITTER_ACCESS_KEY'],
        'ACCESS_SECRET': env['TWITTER_ACCESS_SECRET']
    }
    dry_run = env.get('DRY_RUN') is not None
    poster = TweetPoster(twitter_config, qusasat, dry_run=dry_run)
    jsons = poster.post()
    length = len(jsons)
    tweet_s = 'tweet' if length == 1 else 'tweets'
    print("Posted {} {}".format(length, tweet_s))
    for idx, json in enumerate(jsons, 1):
        print("Tweet {}: {}".format(idx, str(json)))
