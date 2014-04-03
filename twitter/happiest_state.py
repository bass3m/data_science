import sys
import json

scores = {}

# initialize term sentiment dict
state_dict = {}

def sum_sentiments(tweet_words):
    return sum([scores.get(w,0) for w in tweet_words])

def get_tweet_words(tweet):
    """ 
    Returns a list of words, eliminating non alphanumeric chars
    """
    return [w.lower() for w in tweet.split(" ") if w.isalpha()]

def is_en_and_us_tweet(tw):
    return (tw.get(u'place') and tw[u'place'].has_key(u'country_code') and \
            tw[u'place'][u'country_code'] == u'US')

def state(tw):
    return tw[u'place'][u'full_name'].split(', ')[-1]

def state_tweets(tweets):
    """
    Returns term sentiment given the json'd tweets
    """
    for tw in tweets:
        if is_en_and_us_tweet(tw):
            st = state(tw)
            if len(st) == 2:
                words = get_tweet_words(tw['text'])
                sentiment_sum = sum_sentiments(words)
                state_dict[state(tw)] = state_dict.get(state(tw),0) + sentiment_sum

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

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse_sentiment_file(sent_file)
    state_tweets(parse_raw_tweets(tweet_file))
    sorted_states = sorted(state_dict,
                           cmp=lambda x,y : state_dict[x] - state_dict[y],
                           reverse=True)
    if len(sorted_states) > 0:
        print "%s" % (sorted_states[0].strip().replace(' ', '%20').encode('utf-8'))

if __name__ == '__main__':
    main()
