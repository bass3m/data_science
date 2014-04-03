import sys
import json

# initialize term sentiment dict
word_dict = {}

def sum_words():
    return sum([word_dict.get(w,0) for w in word_dict])

def get_tweet_words(tweet):
    """ 
    Returns a list of words, eliminating non alphanumeric chars
    """
    return [w.lower() for w in tweet.split(" ") if w.isalpha()]

def process_words(tweets):
    """
    Returns term sentiment given the json'd tweets
    """
    for tw in tweets:
        if tw.has_key(u'lang') and tw[u'lang'] == u'en':
            words = get_tweet_words(tw['text'])
            for word in words:
                word_dict[word] = word_dict.get(word,0) + 1

def parse_raw_tweets(raw_tweets_file):
    """
    Returns list containing json'd tweets
    """
    all_tweets = raw_tweets_file.readlines()
    return (json.loads(raw_tweet) for raw_tweet in all_tweets)

def get_word_frequency(word):
    """
    Never have to worry about divide by zero, since we must
    have at least 1 tweet. That means deno can never be zero.
    """
    return float(word_dict[word])/float(sum_words())

def main():
    tweet_file = open(sys.argv[1])
    process_words(parse_raw_tweets(tweet_file))
    for word in word_dict.iterkeys():
        print "%s %.3f" %(word.replace(' ', '%20').encode('utf-8'),get_word_frequency(word))

if __name__ == '__main__':
    main()
