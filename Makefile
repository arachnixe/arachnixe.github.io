.PHONY: clean tweets

TWEETS_DATA := tweets/tweets.json

clean:
	rm tweets/*.md

tweets: tweets/tweets.json
	./generate.py
