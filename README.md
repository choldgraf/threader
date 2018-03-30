# threader
Easy Twitter threads with Python.

## Installation

You can install threader with `pip`:

`pip install threader`

Alternatively, clone this repository to your computer and then run either:

`python setup.py install`

or run

`pip install -e path/to/cloned/folder`

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
th = Threader(tweets, api, wait=2)
th.send_tweets()
```

The preceding code resulted in the following twitter thread:

https://twitter.com/choldgraf/status/979755644545777664

Enjoy!
