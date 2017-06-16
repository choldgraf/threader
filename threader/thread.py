from TwitterAPI import TwitterAPI
from tqdm import tqdm
import numpy as np
from time import sleep

class Threader(object):
    def __init__(self, tweets, api, user=None, time=None, end_string=True):
        """Create a thread of tweets.

        Note that you will need your Twitter API / Application keys for
        this to work.

        Parameters
        ----------
        tweets : list of strings
            The tweets to send out
        api : instance of TwitterAPI
            An active Twitter API object using the TwitterAPI package.
        user : string | None
            A user to include in the tweets. If None, no user will be
            included.
        time : float | None
            The amount of time to wait between tweets. If None, they will
            be sent out as soon as possible.
        end_string : bool
            Whether to include a thread count at the end of each tweet. E.g.,
            "4/" or "5x".
        """
        # Checks and assign params
        if not isinstance(tweets, list):
            raise ValueError('tweets must be a list')
        if not all(isinstance(it, str) for it in tweets):
            raise ValueError('all items in `tweets` must be a string')
        if len(tweets) < 2:
            raise ValueError('you must pass two or more tweets')
        if not all(len(tweet) < 137 for tweet in tweets):
            raise ValueError("Not all tweets are less than 137 characters")
        self.tweets = tweets
        if isinstance(user, str):
            self._check_user(user)
        self.user = user
        self.time = time
        self.sent = False
        self.end_string = end_string

        if not isinstance(api, TwitterAPI):
            raise ValueError('api must be an instance of TwitterAPI')
        self.api = api

    def _check_user(self, user):
        if user is not None:
            print('Warning: including users in threaded tweets can get your '
                  'API token banned. Use at your own risk!')
        resp = self.api.request('users/lookup', params={'screen_name': user})

        if not isinstance(resp.json(), list):
            err = resp.json().get('errors', None)
            if err is not None:
                raise ValueError('Error in finding username: {}\nError: {}'.format(user, err[0]))

    def send_tweets(self):
        """Send the queued tweets to twitter."""
        if self.sent is True:
            raise ValueError('Already sent tweets, re-create object in order to send more.')
        self.tweet_ids_ = []
        self.responses_ = []
        self.params_ = []

        # Set up user ID to which we'll tweet
        user = '@{} '.format(self.user) if isinstance(self.user, str) else ''

        # Now generate the tweets
        for ii, tweet in tqdm(enumerate(self.tweets)):
            this_status = '{}{}'.format(user, tweet)

            # Create threading string
            if self.end_string is True:
                thread_char = '/' if tweet != self.tweets[-1] else 'x'
                end_str = '{}{}'.format(ii + 1, thread_char)
                this_status += ' {}'.format(end_str)

            # Create tweet and add metadata
            params = {'status': this_status}
            if len(self.tweet_ids_) > 0:
                params['in_reply_to_status_id'] = self.tweet_ids_[-1]

            # Send POST and get response
            resp = self.api.request('statuses/update', params=params)
            if 'errors' in resp.json().keys():
                raise ValueError('Error in posting tweets:\n{}'.format(
                    resp.json()['errors'][0]))
            self.responses_.append(resp)
            self.params_.append(params)
            self.tweet_ids_.append(resp.json()['id'])
            if isinstance(self.time, (float, int)):
                sleep(self.time)
        self.sent = True

    def __repr__(self):
        s = ['Threader']
        s.append('Tweets: {}'.format(self.tweets))
        if isinstance(self.user, str):
            s.append('Username: {}')
        s = '\n'.join(s)
        return s
