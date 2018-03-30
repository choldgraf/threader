# threader
Easy Twitter threads with Python.

## Installation
Currently the only way to install is by cloning this repository to your
computer and then running either:

`python setup.py install`

or running

`pip install -e path/to/cloned/folder`

This will hopefully change in the future.

## Usage

Threader basically does one thing, illustrated by the following:

```python
from TwitterAPI import TwitterAPI
from threader import Threader

keys = dict(consumer_key='XXX',
            consumer_secret='XXX',
            access_token_key='XXX',
            access_token_secret='XXX')
api = TwitterAPI(**keys)

tweets = ["Chris is testing a nifty little tool he made...",
          "It's for making it easier for him to thread tweets",
          "He heard that the real twitter power users all thread their tweets like pros",
          "but he also likes python, and automating things",
          "sometimes with unnecessary complexity...",
          "so let's see if this works :-D"]
th = Threader(tweets, api, wait=2, user=username)
th.send_tweets()
```

The preceding code resulted in the following twitter thread:

https://twitter.com/choldgraf/status/979755644545777664

Enjoy!
