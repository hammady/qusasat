from os import environ as env
import string
from qusasat import Qusasat
import tweepy


class TweetPoster():
    def __init__(self, twitter_config, qusasat):
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

    def post(self):
        quote = self._get_suitable_quote()
        formatted = self._format_quote(quote)
        print('About to tweet:', formatted)
        return self._api.update_status(status=formatted)

    def _get_suitable_quote(self):
        while True:
            quote = self._qusasat.get_random_quote()
            hashtag = self.to_hashtag(quote['category'])
            if len(quote['quote']) + len(hashtag) + 1 < 280:
                quote['hashtag'] = hashtag
                return quote

    def _format_quote(self, quote):
        return '{}\n{}'.format(quote['quote'], quote['hashtag'])

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
    poster = TweetPoster(twitter_config, qusasat)
    response = poster.post()
    print("Posted a tweet:", str(response))
