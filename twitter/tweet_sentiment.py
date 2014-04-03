import sys
import json

# word sentiment scores
scores = {}

def sum_sentiments(tweet_words):
    return sum([scores.get(w,0) for w in tweet_words])

def get_tweet_words(tweet):
    """ 
    Returns a list of words, eliminating non alphanumeric chars
    """
    return [w.lower() for w in tweet.split(" ") if w.isalpha()]

def get_tweet_sentiment(tweets):
    for tw in tweets:
        # filter out non eng lang tweets
        if tw.has_key(u'lang') and tw[u'lang'] == u'en':
            yield float(sum_sentiments(get_tweet_words(tw['text'])))
        else:
            yield float(0)

def parse_raw_tweets(raw_tweets_file):
    """
    Returns list containing json'd tweets
    """
    all_tweets = raw_tweets_file.readlines()
    return (json.loads(raw_tweet) for raw_tweet in all_tweets)

def parse_sentiment_file(sent_file):
    """
    Populate score dict containing sentiment values
    """
    for line in sent_file:
        term, score  = line.split("\t")
        scores[term] = int(score)

# XXX should add defaults
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse_sentiment_file(sent_file)
    for sentiment in get_tweet_sentiment(parse_raw_tweets(tweet_file)):
        print sentiment

if __name__ == '__main__':
    main()
